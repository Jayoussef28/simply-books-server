from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from simplybooksapi.models import Book, Author, Genre


class BookView(ViewSet):

    def retrieve(self, request, pk):
        """Handle GET requests for single book

        Returns:
            Response -- JSON serialized book
        """
        try:
            book = Book.objects.get(pk=pk)
            genres = Genre.objects.filter(bookId__book_id=book)
            book.genres=genres.all()
            
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all books

        Returns:
            Response -- JSON serialized list of books
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
        
      
    def create(self, request):

        author = Author.objects.get(pk=request.data["author_id"])

        book = Book.objects.create(
            title=request.data["title"],
            image=request.data["image"],
            price=request.data["price"],
            sale=request.data["sale"],
            uid=request.data["uid"],
            description=request.data["description"],
            author=author,
            
        )
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  

    def update(self, request, pk):

        book = Book.objects.get(pk=pk)
        book.title = request.data["title"]
        book.image = request.data["image"]
        book.price = request.data["price"]
        book.sale = request.data["sale"]
        book.uid = request.data["uid"]
        book.description = request.data["description"]
        
        author = Author.objects.get(pk=request.data["author_id"])
        book.author = author
        book.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        book = Book.objects.get(pk=pk)
        book.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ( 'id', 'description')
        

class BookSerializer(serializers.ModelSerializer):

    genres = GenreSerializer(many=True)
    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'image', 'price', 'sale', 'uid', 'description', 'genres')
        depth = 1
