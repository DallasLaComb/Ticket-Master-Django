from django.shortcuts import render
import requests
from django.http import HttpResponseRedirect, JsonResponse
from .models import BookmarkedEvent
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
def get_preferred_image(images):
    for image in images:
        if image.get('ratio') == '16_9' and image.get('width') > 1024:
            return image.get('url')
    return images[0].get('url', 'N/A') if images else 'N/A'

def homepage_view(request):
    context = {
        'events': [],
        'error_message': '',
        'genre_artist_event': '',
        'city': ''
    }
    if 'genreArtistEvent' in request.GET and 'city' in request.GET:
        genre_artist_event = request.GET.get('genreArtistEvent')
        city = request.GET.get('city')
        if not genre_artist_event or not city:
            context['error_message'] = 'Search term and city cannot be empty'
        else:
            api_key = settings.TICKET_MASTER_API_KEY
            url = f'https://app.ticketmaster.com/discovery/v2/events.json?apikey={api_key}&classificationName={genre_artist_event}&city={city}&sort=date,asc'
            try:
                response = requests.get(url)
                data = response.json()
                if '_embedded' in data and 'events' in data['_embedded']:
                    for event in data['_embedded']['events']:
                        event_info = {
                            'event_name': event.get('name', 'N/A'),
                            'local_date': event['dates']['start'].get('localDate', 'N/A'),
                            'local_time': event['dates']['start'].get('localTime', 'N/A'),
                            'image_url': get_preferred_image(event.get('images', [])),
                            'url': event.get('url', '#'),
                        }

                        venue_info = event.get('_embedded', {}).get('venues', [{}])[0]
                        event_info.update({
                            'venue': venue_info.get('name', 'N/A'),
                            'city': venue_info.get('city', {}).get('name', 'N/A'),
                            'state': venue_info.get('state', {}).get('stateCode', 'N/A'),
                            'postal_code': venue_info.get('postalCode', 'N/A'),
                        })

                        context['events'].append(event_info)
                else:
                    context['error_message'] = 'No events found.'

            except requests.RequestException as e:
                context['error_message'] = f'Error fetching data: {str(e)}'

            for event in context['events']:
                    event['is_bookmarked'] = BookmarkedEvent.objects.filter(
                        event_name=event['event_name'],
                        city=event['city'],
                        state=event['state']
                    ).exists()

            context['genre_artist_event'] = genre_artist_event
            context['city'] = city
    return render(request, 'index.html', context)

@require_http_methods(["POST"])
def bookmark_event(request):
    event_data = request.POST
    # Create a new BookmarkedEvent instance
    new_bookmark = BookmarkedEvent(
        event_name=event_data.get('event_name'),
        local_date=event_data.get('local_date'),
        local_time=event_data.get('local_time'),
        venue=event_data.get('venue'),
        city=event_data.get('city'),
        state=event_data.get('state'),
        postal_code=event_data.get('postal_code'),
        image_url=event_data.get('image_url'),
    )
    new_bookmark.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def bookmarks_view(request):
    bookmarks = BookmarkedEvent.objects.all() 
    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})

def edit_note(request, bookmark_id):
    if request.method == 'POST':
        bookmark = get_object_or_404(BookmarkedEvent, id=bookmark_id)
        bookmark.note = request.POST.get('note', '')
        bookmark.save()
        return redirect('bookmarks')

def delete_bookmark(request, bookmark_id):
    if request.method == 'POST':
        bookmark = get_object_or_404(BookmarkedEvent, id=bookmark_id)
        bookmark.delete()
        return redirect('bookmarks')
