from django.utils.deprecation import MiddlewareMixin

class ResetNoOfSlotMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the response has an error status code
        if response.status_code >= 400:
            self.reset_no_of_slots()
        return response

    def reset_no_of_slots(self):
        from thesis.models import ProgramSlot  # Import within function to avoid AppRegistryNotReady
        ProgramSlot.objects.update(no_of_slot=0)
        print("All no_of_slot fields have been reset to 0.")
