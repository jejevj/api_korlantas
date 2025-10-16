from flask import request, jsonify
from ...extensions import db
from ...models.cfd import Cfd
from ...models.genpdf import Genpdf  # Assuming you have a Genpdf model
from ...models.xdata import XData  # Assuming you have a Xdata model
from ...models.master_core import MasterCore  # Assuming you have a MasterCore model
from ...models.vehicles import Vehicle  # Assuming you have a MasterCore model
from ...models.map_user_vehicle import MapUserVehicle  # Assuming you have a MasterCore model
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
    data = request.form
    files = request.files

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return bad_request("Authorization token is missing")

    token = auth_header.split(" ")[1]
    if is_token_blacklisted(token):
        return unauthorized("Token has been invalidated (blacklisted)")

    try:
        user_data = decode_token(token)
        changed_by = user_data.get("username")
        user_id = user_data.get("user_id")
        print("hI")
        print(changed_by)
        company_id_from_token = user_data.get("company_id")
        location_id_from_token = user_data.get("location_id")
    except Exception:
        return unauthorized("Invalid or expired token")

    # Data validation
    required_fields = ["valid_content", "jenis_ranmor", "nomor_rangka", "nomor_mesin", "plat_nomor"]
    missing_fields = [f for f in required_fields if f not in data or not data[f]]
    if missing_fields:
        return bad_request(f"Missing required field(s): {', '.join(missing_fields)}")

    for key in ["nomor_rangka_pic", "nomor_mesin_pic", "tampak_depan_pic", "tampak_belakang_pic"]:
        if key not in files:
            return bad_request("Missing required image file(s)")

    # Saving images
    nomor_rangka_pic_path = save_image(files['nomor_rangka_pic'], 'nomor_rangka')
    nomor_mesin_pic_path = save_image(files['nomor_mesin_pic'], 'nomor_mesin')
    tampak_depan_pic_path = save_image(files['tampak_depan_pic'], 'tampak_depan')
    tampak_belakang_pic_path = save_image(files['tampak_belakang_pic'], 'tampak_belakang')

    try:
        # Insert into `cfd`
        cfd = Cfd(            
            # master_id=new_cfd_id,  # Add master_id as cfd.id
            valid_content=str(data["valid_content"]).lower() in ("true", "1", "t", "yes"),
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
        db.session.flush()  # Get cfd.id
        new_cfd_id = cfd.id
        
# Now you can safely use new_cfd_id for master_id
        cfd.master_id = new_cfd_id


        # Insert into `vehicles`
        vehicle = Vehicle(
            status=1,  # Assuming '1' is the default status
            user_id=user_id,  # Assuming 150 is the user_id
            cfd_id=new_cfd_id,
            genpdf_id=None,  # Assuming genpdf_id is optional or will be set later
            merk=None,  # Example field, replace with actual data
            tipe=None,  # Example field, replace with actual data
            jenis=None,  # Example field, replace with actual data
            model=None,  # Example field, replace with actual data
            tahun_pembuatan=None,  # Example field, replace with actual data
            isi_daya=None,  # Example field, replace with actual data
            warna=None,  # Example field, replace with actual data
            bahan_bakar=None,  # Example field, replace with actual data
            jumlah_sumbu=None,  # Example field, replace with actual data
            jumlah_roda=None,  # Example field, replace with actual data
            created_at=db.func.now(),
            updated_at=db.func.now(),
            changed_by=changed_by,
            verified_at=None,  # Example field, replace with actual data
            sent_at=None,  # Example field, replace with actual data
            verified_by=None  # Example field, replace with actual data
        )
        db.session.add(vehicle)
        db.session.flush()  # Get vehicle.id
        new_vehicle_id = vehicle.id

        # Insert into `map_user_vehicle`
        map_user_vehicle = MapUserVehicle(
            id= new_cfd_id,  
            user_id= user_id,  
            vehicle_id=new_vehicle_id,
            created_at=db.func.now(),
            updated_at=db.func.now(),
            changed_by=changed_by
        )
        db.session.add(map_user_vehicle)

       # Ensure numeric fields are either valid or set to None
        xdata = XData(
            id = new_cfd_id,
            master_id=new_cfd_id,
            valid_content=str(data["valid_content"]).lower() in ("true", "1", "t", "yes"),
            merk=data.get("merk", None),  # Use None if the field is missing
            tipe=data.get("tipe", None),
            jenis=data.get("jenis", None),
            model=data.get("model", None),
            tahun_pembuatan=data.get("tahun_pembuatan", None) if data.get("tahun_pembuatan") else None,  # Ensure numeric fields are set to None if empty
            isi_daya=data.get("isi_daya", None),
            warna=data.get("warna", None),
            bahan_bakar=data.get("bahan_bakar", None),
            jumlah_sumbu=int(data.get("jumlah_sumbu", 0)) if data.get("jumlah_sumbu") else None,  # Convert to int or set to None
            jumlah_roda=int(data.get("jumlah_roda", 0)) if data.get("jumlah_roda") else None,  # Convert to int or set to None
            created_at=db.func.now(),
            updated_at=db.func.now(),
            changed_by=changed_by
        )
        db.session.add(xdata)
        db.session.flush()  # Get xdata.id
        new_xdata_id = xdata.id

        # Insert into `genpdf`
        genpdf = Genpdf(
            id = new_cfd_id,
            master_id=new_cfd_id,
            valid_content=str(data["valid_content"]).lower() in ("true", "1", "t", "yes"),
            pdf_format1=None,  # Replace with actual values if applicable
            pdf_format2=None,  # Replace with actual values if applicable
            pdf_format3=None,  # Replace with actual values if applicable
            created_at=db.func.now(),
            updated_at=db.func.now(),
            changed_by=changed_by
        )
        db.session.add(genpdf)
        db.session.flush()  # Get genpdf.id
        new_genpdf_id = genpdf.id

        # Insert into `master_core`
        master_core = MasterCore(
            id = new_cfd_id,
            company_id=data['company_id'],
            location_id=data['location_id'],
            cfd_id=new_cfd_id,
            xdata_id=new_cfd_id,
            genpdf_id=new_cfd_id
        )
        db.session.add(master_core)
        db.session.flush()  # Get master_core.id
        new_master_id = master_core.id

        # Insert into `master_dyn`
        master_dyn = MasterDyn(
            master_id=new_cfd_id,
            inspected_id= user_id,
            status_id=3,  # Assuming '3' is the status id
            updated_at=db.func.now(),
            changed_by=changed_by,
            inspected_at = db.func.now()
        )
        db.session.add(master_dyn)

        db.session.commit()

        response_data = {
            "cfd": {
                "id": cfd.id,
                "master_id": cfd.master_id,  # Assuming `master_id` exists in the `cfd` table
                "valid_content": cfd.valid_content,
                "jenis_ranmor": cfd.jenis_ranmor,
                "nomor_rangka": cfd.nomor_rangka,
                "nomor_mesin": cfd.nomor_mesin,
                "nomor_rangka_pic": cfd.nomor_rangka_pic,
                "nomor_mesin_pic": cfd.nomor_mesin_pic,
                "tampak_depan_pic": cfd.tampak_depan_pic,
                "tampak_belakang_pic": cfd.tampak_belakang_pic,
                "plat_nomor": cfd.plat_nomor,
                "created_at": cfd.created_at,
                "updated_at": cfd.updated_at,
                "changed_by": cfd.changed_by
            },
            "map_user_vehicle": {
                "id": map_user_vehicle.id,
                "user_id": map_user_vehicle.user_id,
                "vehicle_id": map_user_vehicle.vehicle_id,
                "created_at": map_user_vehicle.created_at,
                "updated_at": map_user_vehicle.updated_at,
                "changed_by": map_user_vehicle.changed_by
            },
            "xdata": {
                "id": xdata.id,
                "master_id": xdata.master_id,  # Assuming `master_id` exists in the `xdata` table
                "valid_content": xdata.valid_content,
                "merk": xdata.merk,
                "tipe": xdata.tipe,
                "jenis": xdata.jenis,
                "model": xdata.model,
                "tahun_pembuatan": xdata.tahun_pembuatan,
                "isi_daya": xdata.isi_daya,
                "warna": xdata.warna,
                "bahan_bakar": xdata.bahan_bakar,
                "jumlah_sumbu": xdata.jumlah_sumbu,
                "jumlah_roda": xdata.jumlah_roda,
                "created_at": xdata.created_at,
                "updated_at": xdata.updated_at,
                "changed_by": xdata.changed_by
            },
            "genpdf": {
                "id": genpdf.id,
                "master_id": genpdf.master_id,
                "valid_content": genpdf.valid_content,
                "pdf_format1": genpdf.pdf_format1,  # Assuming `pdf_format1`, `pdf_format2`, and `pdf_format3` exist
                "pdf_format2": genpdf.pdf_format2,
                "pdf_format3": genpdf.pdf_format3,
                "created_at": genpdf.created_at,
                "updated_at": genpdf.updated_at,
                "changed_by": genpdf.changed_by
            },
            "master_core": {
                "id": master_core.id,
                "cfd_id": master_core.cfd_id,
                "xdata_id": master_core.xdata_id,
                "genpdf_id": master_core.genpdf_id,
                "company_id": master_core.company_id,
                "location_id": master_core.location_id,
                "created_at": master_core.created_at
            },
            "master_dyn": {
                "master_id": master_dyn.master_id,
                "status_id": master_dyn.status_id,
                "inspected_id": master_dyn.inspected_id,  # Assuming `inspected_id` exists in the `master_dyn` table
                "inspected_at": master_dyn.inspected_at,
                "verified_id": master_dyn.verified_id,
                "verified_at": master_dyn.verified_at,
                "sent_at": master_dyn.sent_at,
                "updated_at": master_dyn.updated_at,
                "changed_by": master_dyn.changed_by
            }
        }


        return ok(response_data, "Vehicle and related records created successfully")

    except Exception as e:
        db.session.rollback()
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