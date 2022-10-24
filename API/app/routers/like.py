from fastapi import HTTPException, APIRouter, status, Depends, Response
from .. import schemas, models, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(post: schemas.LikePost, db: Session = Depends(get_db), currentUser: int = Depends(oauth2.getCurrentUser)):
    # check if post exist
    susPost = db.query(models.Post).filter(models.Post.id == post.postId).first()
    if not susPost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Couldn't found a post with the id of {post.postId}")

    # getting current state of the post = liked/unliked    
    likeSituation = db.query(models.Likes).filter(models.Likes.post_id == post.postId).filter(models.Likes.user_id == currentUser.id)
    
    # like the post
    if not likeSituation.first() and post.voteDir == 1:
        Entry = models.Likes(post_id=post.postId, user_id=currentUser.id)
        db.add(Entry)
        db.commit()
        db.refresh(Entry)
        return Entry

    elif likeSituation.first() and post.voteDir == 0:
        likeSituation.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    elif likeSituation.first() and post.voteDir == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already liked the post")

    elif not likeSituation.first() and post.voteDir == 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Can't unlike the post")
        
    

