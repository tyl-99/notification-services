"""
Script to check for duplicate tokens in Firestore.
"""

import os
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_service import initialize_firebase

load_dotenv()

def check_duplicates():
    """Check for duplicate tokens and registrations."""
    initialize_firebase()
    db = firestore.client()
    
    # Get all tokens
    docs = db.collection("device_tokens").stream()
    
    tokens_dict = {}
    duplicates = []
    
    print("\n" + "="*80)
    print("CHECKING FOR DUPLICATE TOKENS")
    print("="*80)
    
    for doc in docs:
        data = doc.to_dict()
        token = data.get('token', '')
        doc_id = doc.id
        
        # Check if token appears multiple times
        if token in tokens_dict:
            duplicates.append({
                'token': token,
                'doc_id_1': tokens_dict[token],
                'doc_id_2': doc_id,
                'data_1': tokens_dict[token + '_data'],
                'data_2': data
            })
        else:
            tokens_dict[token] = doc_id
            tokens_dict[token + '_data'] = data
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate token(s):\n")
        for dup in duplicates:
            print(f"Token: {dup['token'][:50]}...")
            print(f"  Document 1: {dup['doc_id_1']}")
            print(f"    App ID: {dup['data_1'].get('app_id')}")
            print(f"    User ID: {dup['data_1'].get('user_id')}")
            print(f"  Document 2: {dup['doc_id_2']}")
            print(f"    App ID: {dup['data_2'].get('app_id')}")
            print(f"    User ID: {dup['data_2'].get('user_id')}")
            print()
    else:
        print("\n✅ No duplicate tokens found!")
    
    # Check for same token registered multiple times with different document IDs
    print("\n" + "="*80)
    print("CHECKING TOKEN REGISTRATION PATTERNS")
    print("="*80)
    
    token_to_docs = {}
    for doc in db.collection("device_tokens").stream():
        data = doc.to_dict()
        token = data.get('token', '')
        if token not in token_to_docs:
            token_to_docs[token] = []
        token_to_docs[token].append({
            'doc_id': doc.id,
            'app_id': data.get('app_id'),
            'user_id': data.get('user_id'),
            'created_at': data.get('created_at')
        })
    
    multiple_registrations = {k: v for k, v in token_to_docs.items() if len(v) > 1}
    
    if multiple_registrations:
        print(f"\n⚠️  Found {len(multiple_registrations)} token(s) registered multiple times:\n")
        for token, docs_list in multiple_registrations.items():
            print(f"Token: {token[:50]}...")
            print(f"  Registered {len(docs_list)} times:")
            for i, doc_info in enumerate(docs_list, 1):
                print(f"    {i}. Doc ID: {doc_info['doc_id']}")
                print(f"       App: {doc_info['app_id']}, User: {doc_info['user_id']}")
            print()
    else:
        print("\n✅ All tokens are unique!")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total tokens: {len(tokens_dict)}")
    print(f"Duplicate tokens: {len(duplicates)}")
    print(f"Tokens with multiple registrations: {len(multiple_registrations)}")
    
    if duplicates or multiple_registrations:
        print("\n💡 SOLUTION:")
        print("The issue is likely that:")
        print("1. Same token is registered multiple times (causing duplicate notifications)")
        print("2. Token registration logic should update existing tokens instead of creating new ones")
        print("\nThe code should handle this, but you may need to clean up duplicates manually.")

if __name__ == "__main__":
    try:
        check_duplicates()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

