from promptpay import qrcode
import os
import logging

logger = logging.getLogger('renthub')


def generate_qr_code(price, room_number):
    """Generate Promptpay QR payment with fixed price."""
    try:
        logger.info(f"Generating QR code for room {room_number} with price {price}")
        payload_with_amount = qrcode.generate_payload("0983923856", price)
        qrcode.to_file(payload_with_amount, f"media/qr_code_images/{room_number}.png")
        logger.info(f"QR code generated successfully for room {room_number}.")
    except Exception as e:
        logger.error(f"Failed to generate QR code: {e}")


def delete_qr_code(room_number):
    """Delete the QR code file for a specific room after receipt submission."""
    qr_code_path = f"media/qr_code_images/{room_number}.png"

    if os.path.exists(qr_code_path):
        os.remove(qr_code_path)
        logger.info(f"QR code for room {room_number} deleted successfully.")
    else:
        logger.debug(f"QR code for room {room_number} not found.")

def get_rental_progress_data(status):
    """Return milestones information regarding rental request approval status."""
    milestones = [
        {"step": 1, "description": "Payment Slip", "status": "Pending", "symbol":""},
        {"step": 2, "description": "Rent Approval", "status": "Pending", "symbol":""},
    ]

    if status == "wait":
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"
    elif status == "approve":
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Approved"
        milestones[1]["symbol"] = "o"

    elif status == "reject":
        milestones[0]["status"] = "Submitted"
        milestones[0]["symbol"] = "o"

        milestones[1]["status"] = "Rejected"
        milestones[1]["symbol"] = "x"

    return milestones