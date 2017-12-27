package main

// Usage: go run correos.go <trackid>

import (
	"encoding/xml"
	"fmt"
	"golang.org/x/text/encoding/charmap"
	"io"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type Response struct {
	XMLOut string `xml:"Body>ConsultaLocalizacionEnviosFasesResponse>ConsultaLocalizacionEnviosFasesResult"`
}

type ConsultaXMLout struct {
	Events []Event `xml:"Respuestas>DatosIdiomas>DatosEnvios>Datos"`
}

type Event struct {
	Status       string `xml:"Estado"`
	Date         string `xml:"Fecha"`
	TrackingCode string `xml:"Codigo,attr"`
	Event        int    `xml:"Evento,attr"`
}

func makeCharsetReader(charset string, input io.Reader) (io.Reader, error) {
	switch charset {
	case "ISO-8859-1":
		// Windows-1252 is a superset of ISO-8859-1, so should do here
	case "Windows-1252":

		return charmap.Windows1252.NewDecoder().Reader(input), nil
	default:
		return nil, fmt.Errorf("Unknown charset: %s", charset)
	}
	return nil, fmt.Errorf("Unknown charset: %s", charset)
}
func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: correos <tracknumber>")
		os.Exit(1)
	}
	shipmentCode := os.Args[1]
	// http://www.correos.es/ss/Satellite/site/aplicacion-magento-de_integracion/detalle_app-sidioma=es_ES
	xmlSend := fmt.Sprintf(`<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<soap:Body>
<ConsultaLocalizacionEnviosFases xmlns="ServiciosWebLocalizacionMI/">
<XMLin><![CDATA[<?xml version="1.0" encoding="utf-8" ?><ConsultaXMLin Idioma="1" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Consulta><Codigo>%s</Codigo></Consulta></ConsultaXMLin>]]></XMLin>
</ConsultaLocalizacionEnviosFases>
</soap:Body>
</soap:Envelope>`, shipmentCode)

	// https://play.golang.org/p/lpht7gSN3k by Henrik-Johansson
	req, err := http.NewRequest("POST", "https://online.correos.es/servicioswebLocalizacionMI/localizacionMI.asmx", strings.NewReader(xmlSend))
	req.Method = "POST"
	//	fmt.Println(req)
	if err != nil {
		fmt.Println(err)
		return
	}

	req.Header.Add("ContentType", "text/xml;charset=UTF-8")
	req.Header.Add("SOAPAction", "")
	client := http.Client{}

	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}

	b, err := ioutil.ReadAll(resp.Body)

	if err != nil {
		fmt.Println(err)
		return
	}

	//	fmt.Println(string(b))
	// https://stackoverflow.com/a/23634278/267777
	res := &Response{}
	err = xml.Unmarshal(b, res)
	fmt.Println(res.XMLOut, err)

	// https://stackoverflow.com/a/34712322/267777
	res2 := &ConsultaXMLout{}
	decoder := xml.NewDecoder(strings.NewReader(res.XMLOut))
	decoder.CharsetReader = makeCharsetReader
	err = decoder.Decode(&res2)
	//	err = xml.Unmarshal([]byte(res.Body.GetResponse.XMLOut), res2)
	for _, v := range res2.Events {
		fmt.Printf("%s: %d %s\n", v.Date, v.Event, v.Status)
	}
}
