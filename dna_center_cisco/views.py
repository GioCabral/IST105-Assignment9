from django.shortcuts import render
from .dnac_manager import DNAC_Manager
from .mongo_logger import log_action, logs_collection

# vamos manter um manager global simples só pra esse exemplo
dnac_manager = DNAC_Manager()


def auth_view(request):
    context = {}
    if request.method == "POST":
        ok, result = dnac_manager.get_auth_token()
        if ok:
            log_action("auth", success=True)
            context["token"] = result
            context["success"] = True
        else:
            log_action("auth", success=False, message=result)
            context["error"] = result

    return render(request, "dna_center_cisco/auth.html", context)


def devices_view(request):
    context = {}
    if not dnac_manager.token:
        context["error"] = "Please authenticate first (go to /auth/)."
        return render(request, "dna_center_cisco/devices.html", context)

    ok, result = dnac_manager.get_network_devices()
    if ok:
        log_action("list_devices", success=True)
        context["devices"] = result
    else:
        log_action("list_devices", success=False, message=result)
        context["error"] = result

    return render(request, "dna_center_cisco/devices.html", context)


def interfaces_view(request):
    context = {}
    ip = request.GET.get("ip") or request.POST.get("ip")

    if request.method == "POST" and ip:
        if not dnac_manager.token:
            context["error"] = "Please authenticate first (go to /auth/)."
        else:
            ok, result = dnac_manager.get_device_interfaces(ip)
            if ok:
                log_action("show_interfaces", ip=ip, success=True)
                context["interfaces"] = result
                context["ip"] = ip
            else:
                log_action("show_interfaces", ip=ip, success=False, message=result)
                context["error"] = result
                context["ip"] = ip

    return render(request, "dna_center_cisco/interfaces.html", context)

def logs_view(request):
    # pega os 50 logs mais recentes
    logs = list(logs_collection.find().sort("timestamp", -1).limit(50))
    context = {"logs": logs}
    return render(request, "dna_center_cisco/logs.html", context)
