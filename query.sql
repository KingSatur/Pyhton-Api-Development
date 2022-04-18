select * from posts c right join votes v on c.id = v.post_id ;
select users.id, COUNT(*) as posts_quantity from posts right join users on posts.user_id = users.id group by users.id;
select users.id, COUNT(posts.user_id) as posts_quantity from posts right join users on posts.user_id = users.id group by users.id;

select * from posts c right join votes v on c.id = v.post_id ;

select posts.*, COUNT(votes.post_id)
from votes right join posts
   on votes.post_id = posts.id
where posts.id = 5
group by posts.id;