"""Standard functions for crud"""
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation

class Crud():
    """Manages the standard functions for crud in modules"""

    def __init__(self, serializer_class, model_class, operation=None, after_save=None):
        if operation is None:
            self.operation = lambda x: x
        else:
            self.operation = operation
        if after_save is None:
            self.after_save = lambda x: x
        else:
            self.after_save = after_save

        self.serializer_class = serializer_class
        self.model_class = model_class

    def add(self, request, action_name):
        """Tries to create a row in the database and returns the result"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            data = self.operation(request.data.copy())
            data_serializer = self.serializer_class(data=data)
            if data_serializer.is_valid():
                data_serializer.save()
                self.after_save(data_serializer)
                return Response(
                    {"success":True, "id":data_serializer.data['id']},
                    status=status.HTTP_201_CREATED,
                    content_type='application/json')

            answer = self.error_data(data_serializer)
            return Response(
                answer,
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )
        return PermissionValidation.error_response_webservice(validation, request)

    def replace(self, request, identifier, action_name):
        """Tries to update a row in the db and returns the result"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            model_obj = self.model_class.objects.get(id=identifier)
            data = self.operation(request.data.copy())
            data_serializer = self.serializer_class(model_obj, data=data)

            if data_serializer.is_valid():
                data_serializer.save()
                self.after_save(data_serializer)
                return Response(
                    {"success":True, "id":identifier},
                    status=status.HTTP_200_OK,
                    content_type='application/json'
                )

            data = self.error_data(data_serializer)
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )
        return PermissionValidation.error_response_webservice(validation, request)

    def get(self, request, identifier, action_name):
        """Return a JSON response with data for the given id"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            model_obj = self.model_class.objects.get(id=identifier)
            data_serializer = self.serializer_class(model_obj)
            model_data = data_serializer.data.copy()
            model_data = self.operation(model_data)

            data = {
                "success":True,
                "data":model_data
            }

            return Response(
                data,
                status=status.HTTP_200_OK,
                content_type='application/json'
            )
        return PermissionValidation.error_response_webservice(validation, request)

    def delete(self, request, identifier, action_name, message):
        """Tries to delete a row from db and returns the result"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            model_obj = self.model_class.objects.get(id=identifier)
            model_obj.delete()
            data = {
                "success": True,
                "message": message
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        return PermissionValidation.error_response_webservice(validation, request)

    def toggle(self, request, identifier, action_name, data_name):
        """Toogles the active state for a given row"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)

        if validation['status']:
            model_obj = self.model_class.objects.get(id=identifier)
            previous = model_obj.active

            if previous:
                message = data_name + " desactivado con exito"
            else:
                message = data_name + " activado con exito"

            model_obj.active = not model_obj.active
            model_obj.save()
            data = {
                "success": True,
                "message": message
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        return PermissionValidation.error_response_webservice(validation, request)

    def picker_search(self, request, action_name):
        """Returns a JSON response with data for a selectpicker."""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            value = request.data['value']

            queryset = self.operation(self.model_class, value)
            serializer = self.serializer_class(queryset, many=True)
            result = serializer.data

            data = {
                "success": True,
                "result": result
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        return PermissionValidation.error_response_webservice(validation, request)

    def listing(self, request, action_name):
        """ Returns a JSON response containing registered users"""
        permission_obj = PermissionValidation(request)
        validation = permission_obj.validate(action_name)
        if validation['status']:
            sent_data = request.data
            draw = int(sent_data['draw'])
            start = int(sent_data['start'])
            length = int(sent_data['length'])
            search = sent_data['search[value]']

            records_total = self.model_class.objects.count()

            if search != '':
                queryset = self.operation(
                    search, start, length
                )
                records_filtered = self.operation(
                    search, start, length, True
                )
            else:
                queryset = self.model_class.objects.all()[start:start + length]
                records_filtered = records_total

            result = self.serializer_class(queryset, many=True)
            data = {
                'draw': draw,
                'recordsTotal': records_total,
                'recordsFiltered': records_filtered,
                'data': result.data
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        return PermissionValidation.error_response_webservice(validation, request)

    @staticmethod
    def error_data(serializer):
        """Return a common JSON error result"""
        error_details = []
        for key in serializer.errors.keys():
            error_details.append({"field": key, "message": serializer.errors[key][0]})

        data = {
            "Error": {
                "success": False,
                "status": 400,
                "message": "Los datos enviados no son validos",
                "details": error_details
            }
        }
        return data
