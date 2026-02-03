
import time
from django.core.cache import cache
from rest_framework.response import Response
from django.http import JsonResponse  # or use DRF Response if you prefer


class RateLimmitMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        self.limit = 5
        self.window = 30

    def __call__(self,request):
        ip = self.get_client_ip(request)
        chache_key = f'rate limit :{ip}'

        current_time = int(time.time())
        data = cache.get(chache_key)

        if  data is None:
            count,start_time = 1,current_time
            cache.set(chache_key,(count,current_time),timeout=self.window)
        else:
            count,start_time = data
            elapsed = current_time - start_time
            if elapsed < self.window:
                if count>=self.limit:
                         return JsonResponse(
                        {"error": "Too many requests. Please try again later."},
                        status=429,
                    )
                
                count+=1
                remaining = max(self.window - elapsed, 1)
                cache.set(chache_key, (count, start_time), timeout=remaining)
            else:
                # window expired → reset counter
                count, start_time = 1, current_time
                cache.set(chache_key, (count, start_time), timeout=self.window) 
        response = self.get_response(request)
        return response           
                     


    def get_client_ip(self,request):
        return request.META.get('REMOTE_ADDR')