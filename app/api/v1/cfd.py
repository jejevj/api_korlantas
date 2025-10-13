from flask import request, jsonify
from ...extensions import db
from ...models.cfd import Cfd
from ...models.genpdf import Genpdf  # Assuming you have a Genpdf model
from ...models.xdata import XData  # Assuming you have a Xdata model
from ...models.master_core import MasterCore  # Assuming you have a MasterCore model
from ...models.master_dyn import MasterDyn  # Assuming you have a MasterDyn model
from ...models.mobile_blacklist_token import MobileBlacklistToken
from ...utils.jwt_helper import decode_token
from ...utils.responses import ok, unauthorized, bad_request
from ...utils.pagination import clamp_per_page
from . import bp
import os
from werkzeug.utils import secure_filename
import uuid




# Define the file upload folder
UPLOAD_FOLDER = 'cfd/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
image_folders = [
    'nomor_rangka',
    'nomor_mesin',
    'tampak_depan',
    'tampak_belakang'
]

for folder in image_folders:
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def is_token_blacklisted(token: str) -> bool:
    """Check if the token is blacklisted."""
    blacklisted_token = MobileBlacklistToken.query.filter_by(token=token).first()
    return blacklisted_token is not None

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(extension: str) -> str:
    # Generate a unique identifier and append the file extension
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    return unique_filename


# Function to save the image based on type
def save_image(file, image_type):
    if file and allowed_file(file.filename):
       # Ensure the image type directory exists
        directory_path = os.path.join(UPLOAD_FOLDER, image_type)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        
        # Extract the file extension
        extension = file.filename.rsplit('.', 1)[1].lower()
        
        # Generate a unique filename using UUID
        unique_filename = generate_unique_filename(extension)
        
        # Create the full file path with the unique filename
        file_path = os.path.join(directory_path, unique_filename)
        
        # Save the file to the directory
        file.save(file_path)
        return file_path
    return None

@bp.post("/cfd")
def create_cfd():
    """
    Create a new CFD record with file uploads (images) and other data.
    """
    data = request.form  # Get the form data (including text fields)
    files = request.files  # Get the file data (images)

    # Get the Authorization token from the headers
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return bad_request("Authorization token is missing")
    
    # Extract the token from the Authorization header
    token = auth_header.split(" ")[1]
    if is_token_blacklisted(token):
        return unauthorized("Token has been invalidated (blacklisted)")
    # Decode the token to get user information
    try:
        user_data = decode_token(token)
        username_from_token = user_data.get("username")
    except Exception as e:
        return unauthorized("Invalid or expired token")
    # Decode the token to get user information
    try:
        user_data = decode_token(token)
        company_id_from_token = user_data.get("company_id")
        location_id_from_token = user_data.get("location_id")
        changed_by = user_data.get("username")
    except Exception as e:
        return bad_request(f"Invalid or expired token: {str(e)}")

    # Validate required fields in form data
    required_fields = ["valid_content", "jenis_ranmor", "nomor_rangka", "nomor_mesin", "plat_nomor"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return bad_request(f"Missing required field(s): {', '.join(missing_fields)}")

    # Check if files are provided and are valid
    if 'nomor_rangka_pic' not in files or 'nomor_mesin_pic' not in files or 'tampak_depan_pic' not in files or 'tampak_belakang_pic' not in files:
        return bad_request("Missing required image file(s)")

    nomor_rangka_pic_path = save_image(files['nomor_rangka_pic'], 'nomor_rangka')
    nomor_mesin_pic_path = save_image(files['nomor_mesin_pic'], 'nomor_mesin')
    tampak_depan_pic_path = save_image(files['tampak_depan_pic'], 'tampak_depan')
    tampak_belakang_pic_path = save_image(files['tampak_belakang_pic'], 'tampak_belakang')

    try:
        # Start a transaction block
        with db.session.begin():
            # Insert into genpdf table with only changed_by field
            genpdf = Genpdf(changed_by=changed_by)
            db.session.add(genpdf)
            db.session.flush()  # Ensure the ID is generated
            new_genpdf_id = genpdf.id

            # Insert into cfd table and return the generated ID
            cfd = Cfd(
                valid_content=data["valid_content"] == 'true',
                jenis_ranmor=data["jenis_ranmor"],
                nomor_rangka=data["nomor_rangka"],
                nomor_mesin=data["nomor_mesin"],
                nomor_rangka_pic=nomor_rangka_pic_path,
                nomor_mesin_pic=nomor_mesin_pic_path,
                tampak_depan_pic=tampak_depan_pic_path,
                tampak_belakang_pic=tampak_belakang_pic_path,
                changed_by=changed_by,
                plat_nomor=data["plat_nomor"]
            )
            db.session.add(cfd)
            db.session.flush()  # Ensure the ID is generated
            new_cfd_id = cfd.id

            # Insert into xdata table and return the generated ID
            xdata = XData(changed_by=changed_by)
            db.session.add(xdata)
            db.session.flush()  # Ensure the ID is generated
            new_xdata_id = xdata.id

            # Insert into master_core table and return the generated ID
            master_core = MasterCore(
                company_id=data['company_id'],  # Use company_id from token
                location_id=data['location_id'],  # Use location_id from token
                cfd_id=new_cfd_id,
                xdata_id=new_cfd_id,
                genpdf_id=new_cfd_id
            )
            db.session.add(master_core)
            db.session.flush()  # Ensure the ID is generated
            new_master_id = master_core.id

            # Insert into master_dyn table
            master_dyn = MasterDyn(
                master_id=new_master_id,
                status_id=0,  # Assuming 'status_id' should be 0 as per your example
                updated_at=db.func.now(),
                changed_by='init'
            )
            db.session.add(master_dyn)

            db.session.commit()

        # Manually serialize the inserted data (create dictionaries)
        cfd_data = {
            "id": cfd.id,
            "valid_content": cfd.valid_content,
            "jenis_ranmor": cfd.jenis_ranmor,
            "nomor_rangka": cfd.nomor_rangka,
            "nomor_mesin": cfd.nomor_mesin,
            "nomor_rangka_pic": cfd.nomor_rangka_pic,
            "nomor_mesin_pic": cfd.nomor_mesin_pic,
            "tampak_depan_pic": cfd.tampak_depan_pic,
            "tampak_belakang_pic": cfd.tampak_belakang_pic,
            "plat_nomor": cfd.plat_nomor,
            "changed_by": cfd.changed_by,
            "created_at": cfd.created_at,
            "updated_at": cfd.updated_at
        }

        xdata_data = {
            "id": xdata.id,
            "changed_by": xdata.changed_by,
            "created_at": xdata.created_at,
            "updated_at": xdata.updated_at
        }

        master_core_data = {
            "id": master_core.id,
            "company_id": master_core.company_id,
            "location_id": master_core.location_id,
            "cfd_id": master_core.cfd_id,
            "xdata_id": master_core.xdata_id,
            "genpdf_id": master_core.genpdf_id
        }

        master_dyn_data = {
            "master_id": master_dyn.master_id,
            "status_id": master_dyn.status_id,
            "updated_at": master_dyn.updated_at,
            "changed_by": master_dyn.changed_by
        }

        # Prepare the response data
        response_data = {
            "cfd": cfd_data,
            "xdata": xdata_data,
            "master_core": master_core_data,
            "master_dyn": master_dyn_data
        }

        return ok(response_data, "CFD record created successfully")
    except Exception as e:
        db.session.rollback()  # Rollback in case of any errors
        return bad_request(f"Error inserting CFD data: {str(e)}")

@bp.post("/cfd/latest")
def get_latest_cfd():
    """
    Retrieve the latest CFD record where changed_by matches, the username is authenticated via bearer token,
    and filter by valid_content (True/False), with pagination.
    """
    # Get the authorization header from the request
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return unauthorized("Authorization token is missing")
    
    # Extract the token from the Authorization header
    token = auth_header.split(" ")[1]
    if is_token_blacklisted(token):
        return unauthorized("Token has been invalidated (blacklisted)")
    # Decode the token to get user information
    try:
        user_data = decode_token(token)
        username_from_token = user_data.get("username")
    except Exception as e:
        return unauthorized("Invalid or expired token")

    # Get the request JSON data (expects "changed_by" and optional "valid_content")
    data = request.get_json(silent=True) or {}
    
    if not isinstance(data, dict):
        return bad_request("Body must be a JSON object")
    
    # Validate required fields
    required_fields = ["changed_by"]
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return bad_request(f"Missing required field(s): {', '.join(missing_fields)}")
    
    changed_by = data["changed_by"]
    valid_content = data.get("valid_content", None)  # Can be 't' for True or 'f' for False
    
    # Convert 'valid_content' to boolean if it's a string 't' or 'f'
    if valid_content == 't':
        valid_content = True
    elif valid_content == 'f':
        valid_content = False
    
    # Pagination: extract page and per_page from the request
    page = data.get("page", 1)  # Default page is 1
    per_page = data.get("per_page", 5)  # Default per_page is 20
    per_page = clamp_per_page(per_page, default=20, maximum=100)  # Clamp per_page to a valid range

    # Build the base query
    query = Cfd.query.filter_by(changed_by=changed_by)

    # Filter by valid_content if provided
    if valid_content is not None:
        query = query.filter_by(valid_content=valid_content)

    # Paginate the query based on page and per_page
    cfd_records = query.order_by(Cfd.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    if not cfd_records.items:
        return bad_request("No matching CFD records found")

    # Return the found CFD records with pagination metadata
    response_data = {
        "page": cfd_records.page,
        "per_page": cfd_records.per_page,
        "total": cfd_records.total,
        "pages": cfd_records.pages,
        "items": [
            {
                "id": cfd.id,
                "master_id": cfd.master_id,
                "valid_content": cfd.valid_content,
                "jenis_ranmor": cfd.jenis_ranmor,
                "nomor_rangka": cfd.nomor_rangka,
                "nomor_mesin": cfd.nomor_mesin,
                "nomor_rangka_pic": cfd.nomor_rangka_pic,
                "nomor_mesin_pic": cfd.nomor_mesin_pic,
                "tampak_depan_pic": cfd.tampak_depan_pic,
                "tampak_belakang_pic": cfd.tampak_belakang_pic,
                "created_at": cfd.created_at,
                "updated_at": cfd.updated_at,
                "changed_by": cfd.changed_by,
                "plat_nomor": cfd.plat_nomor
            }
            for cfd in cfd_records.items
        ]
    }
    
    return ok(response_data, "Latest CFD records retrieved successfully")
