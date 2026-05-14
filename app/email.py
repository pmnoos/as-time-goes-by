import os
import logging
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

# ── Change these to your real details ──
FROM_EMAIL = "autobiography@autobiography.live"
TO_EMAIL   = "petermagner3@gmail.com"  # whatever you actually check

def send_contact_email(name: str, email: str, subject: str, message: str) -> bool:
    """
    Send a contact form submission email via Resend.
    Returns True on success, False on failure.
    """
   
    try:
        params = {
            "from": FROM_EMAIL,
            "to": [TO_EMAIL],
            "reply_to": email,
            "subject": f"[As Time Goes By] {subject}",
            "html": f"""
                <div style="font-family: system-ui, sans-serif; max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #7c3aed, #db2777);
                                padding: 2rem; border-radius: 12px 12px 0 0;">
                        <h1 style="color: #fff; margin: 0; font-size: 1.4rem;">
                            New Contact Message
                        </h1>
                        <p style="color: rgba(255,255,255,0.85); margin: 0.5rem 0 0; font-size: 0.9rem;">
                            As Time Goes By — Contact Form
                        </p>
                    </div>
                    <div style="background: #ffffff; padding: 2rem;
                                border: 1px solid #e5e7eb; border-top: none;
                                border-radius: 0 0 12px 12px;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 0.5rem 0; color: #6b7280;
                                           font-size: 0.85rem; width: 80px;">Name</td>
                                <td style="padding: 0.5rem 0; font-weight: 600;
                                           color: #111827;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 0.5rem 0; color: #6b7280;
                                           font-size: 0.85rem;">Email</td>
                                <td style="padding: 0.5rem 0;">
                                    <a href="mailto:{email}" style="color: #7c3aed;">{email}</a>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 0.5rem 0; color: #6b7280;
                                           font-size: 0.85rem;">Subject</td>
                                <td style="padding: 0.5rem 0; color: #111827;">{subject}</td>
                            </tr>
                        </table>
                        <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 1.5rem 0;">
                        <h3 style="font-size: 0.85rem; color: #6b7280;
                                   text-transform: uppercase; letter-spacing: 0.05em;
                                   margin: 0 0 0.75rem;">Message</h3>
                        <div style="background: #f9fafb; border-radius: 8px;
                                    padding: 1.25rem; color: #374151;
                                    line-height: 1.7; white-space: pre-wrap;">{message}</div>
                        <div style="margin-top: 1.5rem; text-align: center;">
                            <a href="mailto:{email}?subject=Re: {subject}"
                               style="display: inline-block; background: #7c3aed;
                                      color: #fff; padding: 0.6rem 1.5rem;
                                      border-radius: 8px; text-decoration: none;
                                      font-weight: 500; font-size: 0.9rem;">
                                Reply to {name}
                            </a>
                        </div>
                    </div>
                    <p style="text-align: center; color: #9ca3af;
                               font-size: 0.75rem; margin-top: 1rem;">
                        As Time Goes By · Brisbane, Australia
                    </p>
                </div>
            """,
        }
        resend.Emails.send(params)
        return True
    except Exception as e:
        logging.error(f"Resend email failed: {e}")
        return False