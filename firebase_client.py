"""
Firebase client for AATSE state management and data persistence.
Implements robust error handling and connection management.
"""
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, initialize_app
    from google.cloud.firestore_v1 import Client
    from google.cloud.firestore_v1.collection import CollectionReference
except ImportError as e:
    logging.error(f"Firebase admin not installed: {e}")
    raise

from config import config

logger = logging.getLogger(__name__)


class FirebaseClient:
    """Firebase client wrapper with error handling and retry logic"""
    
    def __init__(self):
        self.app = None
        self.db: Optional[Client] = None
        self._initialized = False
        self._initialize_firebase()
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with retry logic"""
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                if not firebase_admin._apps:
                    cred = credentials.Certificate(config.firebase_credentials_path)
                    self.app = initialize_app(cred, {
                        'projectId': config.firebase_project_id
                    })
                
                self.db = firestore.client()
                self._initialized = True
                
                # Test connection
                test_doc = self.db.collection('system_health').document('connection_test')
                test_doc.set({
                    'timestamp': datetime.utcnow().isoformat(),
                    'status': 'connected'
                },