from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Genre, Book


class GenreView(ViewSet):
    """Tuna api genre view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single genre

        Returns:
            Response -- JSON serialized genre
        """
        try:
            genre = Genre.objects.get(pk=pk)
            books = Book.objects.filter(genreId__genre_id=genre)
            genre.books=books.all()
            serializer = SingleGenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all genres

        Returns:
            Response -- JSON serialized list of genres
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
        
      
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized genre instance
        """
        genre = Genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  
    
    
    def update(self, request, pk):
        """Handle PUT requests for a song

        Returns:
            Response -- Empty body with 204 status code
        """

        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]
        genre.save()
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

   
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for genres
    """ 
    class Meta:
        model = Genre
        fields = ('id', 'description')

class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'image', 'price', 'sale', 'uid', 'description')
 

class SingleGenreSerializer(serializers.ModelSerializer):
    
    """JSON serializer for songs
    """
    books = BookSerializer(read_only=True, many=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'books')
        depth = 1
