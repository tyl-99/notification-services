"""
Script to check registered tokens in Firestore.
"""

import os
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_service import initialize_firebase

load_dotenv()

def check_tokens():
    """Check all registered tokens."""
    initialize_firebase()
    db = firestore.client()
    
    # Get all tokens
    docs = db.collection("device_tokens").stream()
    
    print("\n" + "="*80)
    print("REGISTERED TOKENS")
    print("="*80)
    
    tokens_by_app = {}
    total_count = 0
    
    for doc in docs:
        total_count += 1
        data = doc.to_dict()
        app_id = data.get('app_id', 'unknown')
        token = data.get('token', '')
        user_id = data.get('user_id', 'N/A')
        device_type = data.get('device_type', 'N/A')
        platform = data.get('platform', 'N/A')
        created_at = data.get('created_at', 'N/A')
        
        if app_id not in tokens_by_app:
            tokens_by_app[app_id] = []
        
        tokens_by_app[app_id].append({
            'token': token,
            'user_id': user_id,
            'device_type': device_type,
            'platform': platform,
            'created_at': created_at,
            'doc_id': doc.id
        })
        
        print(f"\n📱 Token #{total_count}:")
        print(f"   App ID: {app_id}")
        print(f"   User ID: {user_id}")
        print(f"   Device: {device_type} ({platform})")
        print(f"   Created: {created_at}")
        print(f"   Token: {token[:50]}...")
        print(f"   Doc ID: {doc.id}")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total tokens: {total_count}")
    
    for app_id, tokens in tokens_by_app.items():
        print(f"\n{app_id}: {len(tokens)} token(s)")
        for i, token_info in enumerate(tokens, 1):
            print(f"  {i}. {token_info['device_type']} ({token_info['platform']}) - User: {token_info['user_id']}")
            if token_info['token'] == token_info['doc_id']:
                print(f"     ✅ Token matches document ID")
            else:
                print(f"     ⚠️  Token does NOT match document ID!")
    
    # Check for duplicates
    print("\n" + "="*80)
    print("DUPLICATE CHECK")
    print("="*80)
    
    all_tokens = []
    for tokens in tokens_by_app.values():
        for token_info in tokens:
            all_tokens.append(token_info['token'])
    
    seen = set()
    duplicates = []
    for token in all_tokens:
        if token in seen:
            duplicates.append(token)
        seen.add(token)
    
    if duplicates:
        print(f"⚠️  Found {len(duplicates)} duplicate token(s):")
        for dup in duplicates:
            print(f"   - {dup[:50]}...")
    else:
        print("✅ No duplicate tokens found")
    
    # Check for same token registered multiple times
    print("\n" + "="*80)
    print("SAME TOKEN MULTIPLE REGISTRATIONS")
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
            'user_id': data.get('user_id')
        })
    
    for token, docs_list in token_to_docs.items():
        if len(docs_list) > 1:
            print(f"⚠️  Token registered {len(docs_list)} times:")
            print(f"   Token: {token[:50]}...")
            for doc_info in docs_list:
                print(f"   - Doc ID: {doc_info['doc_id']}, App: {doc_info['app_id']}, User: {doc_info['user_id']}")

if __name__ == "__main__":
    try:
        check_tokens()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


