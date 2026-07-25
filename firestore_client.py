import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
import uuid
from passlib.context import CryptContext

cred = credentials.Certificate("secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)



def insert_user_full(first_name: str, last_name: str, email: str, password: str, phone: str, age: int, country: str):
    user_id = str(uuid.uuid4())
    db.collection("users").document(user_id).set({
        "firstName": first_name,
        "lastName": last_name,
        "username": f"{first_name} {last_name}",
        "email": email,
        "passwordHash": hash_password(password),
        "phone": phone,
        "age": age,
        "country": country,
        "createdAt": SERVER_TIMESTAMP,
    })
    print(f"Inserted user: {user_id}")
    return user_id


def get_user_by_email(email: str):
    query = db.collection("users").where("email", "==", email).limit(1).stream()
    for doc in query:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None

def insert_chat_session(user_id: str, topic: str = "General Chat"):
    session_id = str(uuid.uuid4())
    db.collection("chatSessions").document(session_id).set({
        "userId": user_id,
        "sessionTopic": topic,
        "createdAt": SERVER_TIMESTAMP,
        "endedAt": None,
    })
    print(f"Inserted chat session: {session_id}")
    return session_id


def insert_message(session_id: str, sender_type: str, content: str):
    message_id = str(uuid.uuid4())
    db.collection("messages").document(message_id).set({
        "sessionId": session_id,
        "senderType": sender_type,
        "content": content,
        "timestamp": SERVER_TIMESTAMP,
    })
    return message_id

def get_user_by_id(user_id: str):
    doc = db.collection("users").document(user_id).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None