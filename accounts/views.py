from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, LoginSerializer, ImageSerializer
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import FaqSerializer
from .serializers import StateSerializer
from .serializers import FooterSerializer
from .models import Faq
from .models import State
from .models import Footer
from .models import ImageModel
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Authenticate user using username and password
            user = serializer.validated_data

            # Optional: Log the user in (session-based)
            login(request, user)

            # If you're using JWT tokens for authentication
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "refresh_token": str(refresh),
                "access_token": str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaqView(APIView):
    def post(self, request):
        serializer = FaqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFaqView(APIView):
    def get(self, request):
        # Fetch all FAQs from the database
        faqs = Faq.objects.all()

        # Serialize the FAQ data
        serializer = FaqSerializer(faqs, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)

class FaqDetailView(APIView):
    def get(self, request, pk):
        """
        Retrieve a specific FAQ by ID.
        """
        try:
            faq = Faq.objects.get(pk=pk)
            serializer = FaqSerializer(faq)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Faq.DoesNotExist:
            return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        """
        Update a specific FAQ by ID.
        """
        try:
            faq = Faq.objects.get(pk=pk)
            serializer = FaqSerializer(faq, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Faq.DoesNotExist:
            return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)

class FaqDeleteView(APIView):
    def delete(self, request, pk):
        """
        Delete an FAQ by its ID.
        """
        try:

            # Attempt to find the FAQ with the provided pk
            faq = Faq.objects.get(pk=pk)
            faq.delete()  # Delete the FAQ object
            return Response({"message": "FAQ deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Faq.DoesNotExist:
            return Response({"error": "FAQ not found."}, status=status.HTTP_404_NOT_FOUND)


class ImagesView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        if image:
            # Save the image object
            img_obj = ImageModel.objects.create(image=image)

            # Construct the correct URL
            image_url = f"/api/media/{img_obj.image.name}"

            return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)
        return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

class StateView(APIView):
    def post(self, request):
        data = request.data
        serializer = StateSerializer(data=data)

        if serializer.is_valid():
            state = serializer.save()  # Save the instance

            # Construct the correct image URL
            image_url = f"/api/media/{state.image.name}" 

            # Return the response with image URL
            return Response(
                {
                    "id": state.id,
                    "name": state.name,
                    "image_url": image_url,
                    "uploaded_at": state.uploaded_at,
                },
                status=status.HTTP_201_CREATED,
            )

        # Return serializer errors if validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetStateView(APIView):
    def get(self, request):
        states = State.objects.all()  # Fetch all state objects
        serializer = StateSerializer(states, many=True)  # Serialize multiple objects

        # Construct the response to include full image URLs
        response_data = []
        for state in serializer.data:
            image_path = state['image'].replace('media/', '', 1)  
            image_url = request.build_absolute_uri(f"/api/media{image_path}")
            response_data.append({
                "id": state["id"],
                "name": state["name"],
                "image_url": image_url,
                "uploaded_at": state["uploaded_at"],
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
class EditStateView(APIView):
    def get(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            serializer = StateSerializer(state)
            
            # Correct image URL
            image_path = serializer.data['image'].replace('media/', '', 1)  # Remove redundant prefix
            image_url = request.build_absolute_uri(f"/api/media{image_path}")
            
            # Construct response data
            response_data = {
                "id": serializer.data["id"],
                "name": serializer.data["name"],
                "image_url": image_url,
                "uploaded_at": serializer.data["uploaded_at"],
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        except State.DoesNotExist:
            return Response({"error": "State not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            serializer = StateSerializer(state, data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                # Correct image URL in response
                image_path = serializer.data['image'].replace('media/', '', 1)
                image_url = request.build_absolute_uri(f"/api/media{image_path}")
                
                # Construct response data
                response_data = {
                    "id": serializer.data["id"],
                    "name": serializer.data["name"],
                    "image_url": image_url,
                    "uploaded_at": serializer.data["uploaded_at"],
                }
                
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except State.DoesNotExist:
            return Response({"error": "State not found."}, status=status.HTTP_404_NOT_FOUND)
        
class DeleteStateView(APIView):
    def delete(self, request, pk):
        try:
            state = State.objects.get(pk=pk)
            state.delete()
            return Response({"message": "State deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Faq.DoesNotExist:
            return Response({"error": "State not found."}, status=status.HTTP_404_NOT_FOUND)

class AddFooterView(APIView):
    def post(self, request):
        data = request.data
        
        # Check if there is already data in the Footer table
        existing_footer = Footer.objects.first()
        
        if existing_footer:
            # Update the existing footer
            serializer = FooterSerializer(existing_footer, data=data)
            if serializer.is_valid():
                footer = serializer.save()
                
                # Generate image URL
                image_url = request.build_absolute_uri(f"/api/media/{footer.logo.name}")
                
                return Response(
                    {
                        "id": footer.id,
                        "tagline": footer.tagline,
                        "copyright": footer.copyright,
                        "logo": image_url,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create a new footer
            serializer = FooterSerializer(data=data)
            if serializer.is_valid():
                footer = serializer.save()
                
                # Generate image URL
                image_url = request.build_absolute_uri(f"/api/media/{footer.logo.name}")
                
                return Response(
                    {
                        "id": footer.id,
                        "tagline": footer.tagline,
                        "copyright": footer.copyright,
                        "logo": image_url,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
