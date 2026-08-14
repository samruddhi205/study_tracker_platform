from app import app, db
from models import User, Friend

def make_all_friends():
    with app.app_context():
        users = User.query.all()
        print(f"Found {len(users)} users.")
        
        # Get existing friendships to avoid duplicates
        existing_friendships = set()
        all_friends = Friend.query.all()
        for f in all_friends:
            # Add both directions to the set to easily check existence
            existing_friendships.add((f.sender_id, f.receiver_id))
            existing_friendships.add((f.receiver_id, f.sender_id))
            
            # Since we want everyone to be active friends, update any pending/rejected to 'accepted'
            if f.status != 'accepted':
                f.status = 'accepted'
        
        new_friendships_count = 0
        
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                u1 = users[i]
                u2 = users[j]
                
                if (u1.user_id, u2.user_id) not in existing_friendships:
                    new_friend = Friend(
                        sender_id=u1.user_id,
                        receiver_id=u2.user_id,
                        status='accepted'
                    )
                    db.session.add(new_friend)
                    new_friendships_count += 1
                    
        db.session.commit()
        print(f"Successfully added {new_friendships_count} new friendships and ensured they are all 'accepted'.")

if __name__ == '__main__':
    make_all_friends()
