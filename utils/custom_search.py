from rest_framework import filters
from unidecode import unidecode


class CustomTextSearchFilterBackend(filters.SearchFilter):
    search_param = "q"

    def get_search_fields(self, view, request):
        field_param = request.query_params.get("field")
        v_base_name = None
        try:
            v_base_name = view.basename
        except:
            pass
        if v_base_name and v_base_name == "school_class":
            q_string = None
            try:
                q_string = view.request.query_params["q"]
            except:
                pass
            if q_string is not None:
                q_string_list = q_string.split(" ")
                if len(q_string_list) > 1:
                    if unidecode(q_string_list[0]).lower() == "lop":
                        del q_string_list[0]
                        result = " ".join(map(str, q_string_list))

                        # hacky code :( but anhlt request
                        view.request.query_params._mutable = True
                        view.request.query_params["q"] = result
                        view.request.query_params._mutable = False

        if field_param:
            return field_param.split(",")
        return super().get_search_fields(view, request)
