import os
import datetime
from flask import Flask, url_for, redirect, render_template, request, abort, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from repositories.security import generate_sha256_id
from user import User, AdminUser
from repositories.user_repository import list_users, verify, delete_user, add_user
from repositories.note_repository import read_notes, write_note, delete_note, match_user_with_note
from repositories.image_repository import upload_image, list_images, delete_image, match_user_with_image_uid
from repositories.log_repository import log_event, get_logs
from werkzeug.utils import secure_filename
from logging_config import setup_logger
setup_logger()

import logging
logger = logging.getLogger("flask_app")

app = Flask(__name__)
app.config.from_object('config')

# --- Error Handlers ---
@app.errorhandler(401)
def FUN_401(error):
    return render_template("page_401.html"), 401

@app.errorhandler(403)
def FUN_403(error):
    return render_template("page_403.html"), 403

@app.errorhandler(404)
def FUN_404(error):
    return render_template("page_404.html"), 404

@app.errorhandler(405)
def FUN_405(error):
    return render_template("page_405.html"), 405

@app.errorhandler(413)
def FUN_413(error):
    return render_template("page_413.html"), 413

# --- Login  ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "FUN_login"

@login_manager.user_loader
def load_user(user_id):
    if user_id in list_users():
        if user_id.upper() == "ADMIN":
            return AdminUser(user_id)
        return User(user_id)
    return None

# --- Routes ---
@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/public/")
def FUN_public():
    return render_template("public_page.html")

@app.route("/private/")
@login_required
def FUN_private():
    user_id = current_user.get_id()
    notes_list = read_notes(user_id)
    notes_table = zip([x[0] for x in notes_list],
                      [x[1] for x in notes_list],
                      [x[2] for x in notes_list],
                      ["/delete_note/" + x[0] for x in notes_list])

    images_list = list_images(user_id)
    images_table = zip([x[0] for x in images_list],
                      [x[1] for x in images_list],
                      [x[2] for x in images_list],
                      ["/delete_image/" + x[0] for x in images_list])

    return render_template("private_page.html", notes=notes_table, images=images_table)

@app.route("/admin/")
@login_required
def FUN_admin():
    if current_user.is_admin():
        user_list = list_users()
        user_table = zip(range(1, len(user_list)+1),
                         user_list,
                         ["/delete_user/" + u for u in user_list])
        logs = get_logs()
        return render_template("admin.html", users=user_table, logs=logs)
    else:
        return abort(401)

@app.route("/write_note", methods=["POST"])
@login_required
def FUN_write_note():
    write_note(current_user.get_id(), request.form.get("text_note_to_take"))
    logger.info("Note ajoutée")
    return redirect(url_for("FUN_private"))

@app.route("/delete_note/<note_id>", methods=["GET"])
@login_required
def FUN_delete_note(note_id):
    if current_user.get_id() == match_user_with_note(note_id):
        delete_note(note_id)
        logger.info(f"Note supprimée : {note_id}")
    else:
        return abort(401)
    return redirect(url_for("FUN_private"))

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload_image", methods=['POST'])
@login_required
def FUN_upload_image():
    file = request.files.get('file')
    if not file or file.filename == '' or not allowed_file(file.filename):
        flash('Invalid file', category='danger')
        logger.warning("Erreur lors de l'ajout d'une image.'")
        return redirect(url_for("FUN_private"))

    filename = secure_filename(file.filename)
    upload_time = str(datetime.datetime.now())
    image_uid = generate_sha256_id(upload_time + filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_uid + "-" + filename))
    upload_image(image_uid, current_user.get_id(), filename, upload_time)
    logger.info(f"Image ajouté : {filename}")
    return redirect(url_for("FUN_private"))

@app.route("/delete_image/<image_uid>", methods=["GET"])
@login_required
def FUN_delete_image(image_uid):
    if current_user.get_id() == match_user_with_image_uid(image_uid):
        delete_image(image_uid)
        logger.info(f"Image supprimé : {image_uid}")
        image_to_delete = [y for y in os.listdir(app.config['UPLOAD_FOLDER']) if y.split("-", 1)[0] == image_uid][0]
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_to_delete))
    else:
        logger.warning(f"Erreur lors de la suppression de l'image : {image_uid}")
        return abort(401)
    return redirect(url_for("FUN_private"))

@app.route("/login", methods=["POST"])
def FUN_login():
    id_submitted = request.form.get("id").upper()
    if id_submitted in list_users() and verify(id_submitted, request.form.get("pw")):
        login_user(User(id_submitted))
        log_event(id_submitted, "login")
    return redirect(url_for("FUN_root"))

@app.route("/logout/")
@login_required
def FUN_logout():
    logout_user()
    log_event(current_user.get_id(), "logout")
    return redirect(url_for("FUN_root"))

@app.route("/delete_user/<id>/", methods=['GET'])
@login_required
def FUN_delete_user(id):
    if current_user.is_admin():
        if id == "ADMIN":
            return abort(403)
        for f in [x[0] for x in list_images(id)]:
            image_file = [y for y in os.listdir(app.config['UPLOAD_FOLDER']) if y.split("-", 1)[0] == f][0]
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_file))
        delete_user(id)
        log_event(current_user.get_id(), f"delete_user {id}")
        logger.info(f"Utilisateur supprimé : {id}")
        return redirect(url_for("FUN_admin"))
    return abort(401)

@app.route("/add_user", methods=["POST"])
@login_required
def FUN_add_user():
    if current_user.is_admin():
        new_id = request.form.get('id').upper()
        if new_id in list_users() or " " in new_id or "'" in new_id:
            user_list = list_users()
            user_table = zip(range(1, len(user_list)+1), user_list, ["/delete_user/" + u for u in user_list])
            logger.warning(f"Erreur lors de l'ajout de l'utilisateur : {new_id}")
            return render_template("admin.html", id_to_add_is_duplicated=new_id in list_users(), id_to_add_is_invalid=" " in new_id or "'" in new_id, users=user_table)
        add_user(new_id, request.form.get('pw'))
        log_event(current_user.get_id(), f"add_user {new_id}")
        logger.info(f"Utilisateur ajouté : {new_id}")
        return redirect(url_for("FUN_admin"))
    return abort(401)

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1")
