from apps.admin2.urls.book import urlpatterns as book_urls
from apps.admin2.urls.main import urlpatterns as main_urls
from apps.admin2.urls.unit import urlpatterns as unit_urls
from apps.admin2.urls.vocab import urlpatterns as vocab_urls
from apps.admin2.urls.test import urlpatterns as test_urls

urlpatterns = book_urls + main_urls + unit_urls + vocab_urls + test_urls
