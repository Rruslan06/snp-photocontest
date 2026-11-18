from utils.docs_typed_dict import DocsDict
from api.serializers.comment.comment import CommentSerializer



UPDATE_COMMENT: DocsDict = {
    "tags": ["comment"],
    "description": "Изменить свой комментарий",
    "request": CommentSerializer,
    "responses": {200: CommentSerializer},
}



DELETE_COMMENT: DocsDict = {
    "tags": ["comment"],
    "description": "Удалить свой комментарий (если нет ответов)",
    "responses": {204: None},
}