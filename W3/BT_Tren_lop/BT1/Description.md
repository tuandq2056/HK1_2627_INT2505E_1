Resource : users ,profiles ,posts,comments ,tags,followers,following 


collection : posts, tags, users
item: users/{user_id}, posts/{post_id}
sub-resource : posts/{post_id}/comments, users/{user_id}/followers


