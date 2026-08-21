from schemas import Cursor
import base64

def encode(data: Cursor): 
        json_bytes = data.model_dump_json().encode("utf-8")
        encoded_bytes = base64.urlsafe_b64encode(json_bytes)
        return encoded_bytes.decode("ascii")

def decode(encoded_data: str):
        data = base64.urlsafe_b64decode(encoded_data).decode('utf-8')
        print(f'decoded_data: {data}')
        # error handling can be added here for invalid data types 
        res = Cursor.model_validate_json(data)
        return res 
