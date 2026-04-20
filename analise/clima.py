import requests


def obter_nivel_chuva(latitude: float, longitude: float) -> int:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&hourly=rain,precipitation_probability"
        "&forecast_days=1"
        "&timezone=auto"
    )

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()

        chuvas = dados["hourly"]["rain"]
        probabilidades = dados["hourly"]["precipitation_probability"]

        max_chuva = max(chuvas)
        max_prob = max(probabilidades)

        if max_prob >= 70 or max_chuva >= 5:
            return 2 
        elif max_prob >= 40 or max_chuva >= 1:
            return 1 
        else:
            return 0 

    except Exception as e:
        print("Erro ao consultar API:", e)
        return 0


def descrever_nivel(nivel: int) -> str:
    if nivel == 0:
        return "SEM CHUVA"
    elif nivel == 1:
        return "CHUVA FRACA/MODERADA"
    elif nivel == 2:
        return "CHUVA FORTE"
    return "DESCONHECIDO"


def main():
    print("=== CONSULTA DE PREVISÃO DE CHUVA ===")
    print("Digite as coordenadas da cidade desejada.")
    print("Exemplo São Paulo: latitude -23.55 / longitude -46.63")
    print()

    try:
        latitude = float(input("Latitude: ").strip())
        longitude = float(input("Longitude: ").strip())
    except ValueError:
        print("Erro: latitude/longitude inválidas.")
        return

    nivel = obter_nivel_chuva(latitude, longitude)

    print()
    print("Resultado da previsão:", descrever_nivel(nivel))
    print(f"VALOR PARA DIGITAR NO SERIAL DO WOKWI: {nivel}")
    print()
    print("Digite no monitor serial do ESP32:")
    print("0 = sem chuva")
    print("1 = chuva fraca/moderada")
    print("2 = chuva forte")


if __name__ == "__main__":
    main()