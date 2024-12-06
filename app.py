# Importing requirements
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import os, base64


app = Flask(__name__, template_folder='templates', static_folder='static')


# ---------------------------------------------- Homepage Route --------------------------------------------

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        # After setup, return a success message as JSON
        return jsonify({"message": "Setup complete! Environment has been successfully set up."})

    # First view when the user enters the app
    return render_template("homepage.html")


#------------------------------------------- upload route --------------------------------------------------

@app.route('/upload', methods=['GET', 'POST'])
def upload_media():
    UPLOAD_FOLDER = 'uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if request.method == 'POST':
        # Clear previous uploads
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        # Handle video upload
        video_file = request.files.get('video')
        video_path = None
        if video_file:
            video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
            video_file.save(video_path)

        # Handle audio input
        audio_file = request.files.get('audio')
        recorded_audio = request.form.get('recorded_audio')
        audio_path = None

        if audio_file and recorded_audio:
            return "Error: Only one audio input allowed.", 400
        elif audio_file:
            audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(audio_path)
        elif recorded_audio:
            # Decode the recorded audio (base64)
            audio_path = os.path.join(UPLOAD_FOLDER, 'recorded_audio.wav')
            with open(audio_path, 'wb') as f:
                f.write(base64.b64decode(recorded_audio))

        return redirect(url_for('lipsyncing', video_file=video_path, audio_file=audio_path))

    return render_template('upload.html')

#--------------------------------------------- Lipsyncing route --------------------------------------------------------------


@app.route('/lipsyncing', methods=['GET', 'POST'])
def lipsyncing():
    if request.method == 'POST':
        return redirect(url_for('result'))

    return render_template('lipsyncing.html')



#---------------------------------------------- result route --------------------------------------------------------------

@app.route('/result')
def result():
    return render_template('result.html')


#---------------------------------------------- feedback route --------------------------------------------------------------

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


#---------------------------------------------- submit feedback route --------------------------------------------------------------

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    # You can add code here to process/store feedback data
    return redirect(url_for('feedback'))  # Redirect back to feedback or another thank-you page

#--------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run()
