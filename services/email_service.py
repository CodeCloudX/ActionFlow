import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from threading import Thread
from flask import current_app
from config import Config

# -----------------------------
# Core background email task
# -----------------------------
def _send_email_task(app, msg):
    """Send email in background thread with Flask app context."""
    with app.app_context():
        try:
            # SMTP server setup
            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.send_message(msg)
            app.logger.info(f"Background email sent successfully to {msg['To']}")
        except Exception as e:
            app.logger.error(f"Background email sending failed: {e}")

# -----------------------------
# Main send_email function
# -----------------------------
def send_email(to_email, subject, html_message):
    """
    Prepares HTML email and sends it asynchronously in a background thread.
    """
    app = current_app._get_current_object()

    # Create email message
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr(("ActionFlow", Config.MAIL_USERNAME))
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach HTML message
    msg.attach(MIMEText(html_message, "html"))

    # Start background thread
    Thread(target=_send_email_task, args=(app, msg)).start()

# -----------------------------
# Helper email functions
# -----------------------------

def send_org_registration_email(admin_email, org_name, org_unique_id):
    subject = "Organization Registered Successfully"
    message = f"""
<p>Hello,</p>
<p>Your organization "<b>{org_name}</b>" has been successfully registered.</p>
<p>Organization Unique ID: <b>{org_unique_id}</b></p>
<p>Please keep this ID safe. Users can join your organization using this ID.</p>
<p>Regards,<br>
ActionFlow Support Team</p>
"""
    send_email(admin_email, subject, message)

def send_auto_assign_notification(admin_email, complaint_id, resolver_name, category):
    subject = f"High-Priority Complaint Auto-Assigned: {complaint_id}"
    message = f"""
<p>Hello Admin,</p>
<p>A new <b>HIGH-PRIORITY</b> complaint in the '<b>{category}</b>' category has been automatically assigned.</p>
<p>
    - Complaint ID: <b>{complaint_id}</b><br>
    - Assigned To: <b>{resolver_name}</b>
</p>
<p>This assignment was made automatically based on the complaint category. Please review it at your convenience.</p>
<p>Regards,<br>
ActionFlow Support Team</p>
"""
    send_email(admin_email, subject, message)

def send_forgot_password_email(user_email, reset_link):
    subject = "Password Reset Request"
    message = f"""
<p>Hello,</p>
<p>We received a request to <b>reset your password</b>.</p>
<p>Click the link below to reset your password:</p>
<p><a href="{reset_link}">{reset_link}</a></p>
<p>If you did not request this, please ignore this email.</p>
<p>Regards,<br>
ActionFlow Support Team</p>
"""
    send_email(user_email, subject, message)

def send_complaint_resolved_email(user_email, complaint_id, admin_name):
    subject = f"Update on Your Complaint: {complaint_id}"
    message = f"""
<p>Hello,</p>
<p><b>Good news!</b> Your complaint with ID <b>{complaint_id}</b> has been marked as resolved by <b>{admin_name}</b>.</p>
<p>Please log in to your dashboard to view the details and provide feedback if you wish.</p>
<p>If you are satisfied, you may confirm and close the complaint.
Providing feedback is optional and helps us improve our service.</p>
<p><b>If no action is taken within 3 days, the complaint will be automatically closed by the system.</b></p>
<p>Thank you for your patience and cooperation.</p>
<p>Regards,<br>
ActionFlow Support Team</p>
"""
    send_email(user_email, subject, message)
