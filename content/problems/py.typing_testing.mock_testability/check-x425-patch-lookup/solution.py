import types
from unittest.mock import patch


def patch_lookup(ids):
    lib = types.ModuleType("lib")

    def real_get_user(uid):
        return f"real-{uid}"

    lib.get_user = real_get_user

    app = types.ModuleType("app")
    app.get_user = lib.get_user  # like `from lib import get_user`

    def greet(uid):
        return "hi " + app.get_user(uid)

    with patch.object(lib, "get_user", return_value="stub"):
        wrong = [greet(i) for i in ids]

    with patch.object(app, "get_user", return_value="stub") as mocked:
        right = [greet(i) for i in ids]

    called_with = [call.args[0] for call in mocked.call_args_list]
    return [wrong, right, mocked.call_count, called_with]
