from django.urls import path

from lib.drone_hangar.dropbox import mediabox

from .views import document_viewer, subscription, example

urlpatterns = [
    path(r'communique', document_viewer.CommuniqueView.as_view(),
        name="viewer.communique"),
    path(r'subscribe', subscription.submitOrDisplay),
    # path(r'cid/minutes', document_viewer.DocumentList.as_view(),
    #     kwargs={
    #         'links': mediabox.get_url_list(query='cid-minutes', max=12)
    #     },
    #     name='viewer.minutes'
    # )
]
