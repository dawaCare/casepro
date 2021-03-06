from __future__ import unicode_literals

from .views import LabelCRUDL, FaqCRUDL, MessageCRUDL, MessageExportCRUDL, OutgoingCRUDL, ReplyExportCRUDL

urlpatterns = LabelCRUDL().as_urlpatterns()
urlpatterns += MessageCRUDL().as_urlpatterns()
urlpatterns += FaqCRUDL().as_urlpatterns()
urlpatterns += MessageExportCRUDL().as_urlpatterns()
urlpatterns += OutgoingCRUDL().as_urlpatterns()
urlpatterns += ReplyExportCRUDL().as_urlpatterns()
