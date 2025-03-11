from Comments.CommentQuery import LineCommentQuery


query = LineCommentQuery("java")

print(query.parse("wefe\n//asd\nwefwe"))
