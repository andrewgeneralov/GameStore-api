from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Developer, Game, Order
from .serializers import DeveloperSerializer, GameSerializer, OrderSerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    # GET: получение списка с фильтрацией
    def get_queryset(self):
        queryset = Game.objects.all()
        genre = self.request.query_params.get('genre')
        developer_id = self.request.query_params.get('developer')
        is_available = self.request.query_params.get('is_available')

        if genre:
            queryset = queryset.filter(genre=genre)
        if developer_id:
            queryset = queryset.filter(developer_id=developer_id)
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')

        return queryset

    # POST: создание одного ресурса или группы ресурсов
    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # PATCH: обновление одного ресурса или группы ресурсов
    def partial_update(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            updated_objects = []
            for item in request.data:
                obj_id = item.get('id')
                if not obj_id:
                    return Response({'error': 'Каждый элемент должен содержать id'}, status=status.HTTP_400_BAD_REQUEST)
                instance = Game.objects.get(id=obj_id)
                serializer = self.get_serializer(instance, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_objects.append(serializer.data)
            return Response(updated_objects, status=status.HTTP_200_OK)
        return super().partial_update(request, *args, **kwargs)

    # DELETE: удаление одного ресурса или группы ресурсов
    def destroy(self, request, *args, **kwargs):
        ids = request.data.get('ids', None) if isinstance(request.data, dict) else None
        if ids and isinstance(ids, list):
            deleted_count, _ = Game.objects.filter(id__in=ids).delete()
            return Response({'message': f'Успешно удалено объектов: {deleted_count}'}, status=status.HTTP_200_OK)
        return super().destroy(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer