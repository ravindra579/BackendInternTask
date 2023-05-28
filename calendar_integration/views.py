from django.shortcuts import render
from django.views import View
from google_auth_oauthlib.flow import InstalledAppFlow
from django.http import JsonResponse
from google.auth.transport.requests import Request


# Create your views here.
class GoogleCalendarInitView(View):
    def get(self, request):
        # Define the required OAuth2 scopes
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        
        # Create an OAuth2 flow object
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/backendTask.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
        )
        
        # Generate the authorization URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        
        # Redirect the user to the authorization URL
        return JsonResponse({'auth_url': auth_url})
    
class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Get the authorization code from the request
        code = request.GET.get('code', None)
        
        # Exchange the authorization code for an access token
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials/backendTask.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri='http://localhost:8000/rest/v1/calendar/redirect/'
        )
        flow.fetch_token(code=code)
        
        # Check if the access token has expired, and refresh if necessary
        if flow.credentials and flow.credentials.expired and flow.credentials.refresh_token:
            flow.credentials.refresh(Request())
        
        # Use the access token to get a list of events from the user's calendar
        # Implement the logic to fetch events using the Google Calendar API
        # events = get_events_from_calendar(flow.credentials)
        
        # Return the list of events as a JSON response
        # return JsonResponse({'events': events})
        return JsonResponse({'message': 'Access token obtained successfully'})


