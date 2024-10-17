import pandas as pd
import re
import csv

def decrypt_caesar_cipher(text, shift):
    """Decrypt the Caesar cipher with a given shift."""
    decrypted_text = ''
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def decrypt_emails(filtered_ibans_file, output_file):
    """Decrypt emails using the phone number's last two digits."""
    decrypted_emails = []
    # The correct order of users for decryption
    target_users = [23, 36, 412, 426, 844, 935, 1273]

    # Read the CSV file (assuming it contains necessary data)
    df = pd.read_csv(filtered_ibans_file)

    for index, row in df.iterrows():
        # Extract the numeric part of the 'User' field
        user_str = row['User']
        user = int(re.search(r'\d+', user_str).group())  # Extract digits

        # Process only the specified target users
        if user in target_users:
            phone_number = row['PhoneNumber']

            # Use last two digits of the phone number as Caesar cipher shift
            shift = int(phone_number[-2:]) % 26

            # Decrypt the email
            decrypted_email = decrypt_caesar_cipher( shift)
            decrypted_emails.append([user, decrypted_email])

    # Save decrypted emails to a CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'DecryptedEmail'])  # Header
        writer.writerows(decrypted_emails)

    print(f"Decrypted {len(decrypted_emails)} emails.")

def main():
    # Decrypt the emails using the phone numbers from filtered_ibans.csv
    decrypt_emails('filtered_ibans.csv', 'data/decrypted_emails.csv')

if __name__ == '__main__':
    main()