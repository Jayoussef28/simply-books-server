from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import BookGenre, Book, Genre


class BookGenreView(ViewSet):


    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
            Response -- JSON serialized song
        """
        try:
            book_genre = BookGenre.objects.get(pk=pk)
            serializer = BookGenreSerializer(book_genre)
            return Response(serializer.data)
        except BookGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
            Response -- JSON serialized list of songs
        """
        book_genres = BookGenre.objects.all()
        serializer = BookGenreSerializer(book_genres, many=True)
        return Response(serializer.data)
      
    def create(self, request):

        bookgenre = Book.objects.get(pk=request.data["book_id"])
        genrebook = Genre.objects.get(pk=request.data["genre_id"])
        
        book_genre = BookGenre.objects.create(
            book=bookgenre,
            genre=genrebook,
        )
        serializer = BookGenreSerializer(book_genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
      
        bookgenre = Book.objects.get(pk=request.data["book"])
        genrebook = Genre.objects.get(pk=request.data["genre"])

        book_genre = BookGenre.objects.get(pk=pk)
        book_genre.book_id = bookgenre
        book_genre.genre_id = genrebook

        book_genre.save()
        serializer = BookGenreSerializer(book_genre)
        return Response(serializer.data, status=status.HTTP_200_OK)  
      
      
    def destroy(self, request, pk):
        book_genre = BookGenre.objects.get(pk=pk)
        book_genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    

class BookGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres
    """
    class Meta:
        model = BookGenre
        fields = ('id', 'book', 'genre')
        depth = 1
