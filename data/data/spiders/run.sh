#/bin/bash
for s in user_followed following_user user_following user_star repo_star followed_user star_user star_repo
do
	scrapy crawl $s > log/$s.log &
done
