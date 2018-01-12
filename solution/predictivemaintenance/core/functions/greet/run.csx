#load "..\CiqsHelpers\All.csx"

using System.Net;

public static async Task<object> Run(HttpRequestMessage req, TraceWriter log)
{
    var parametersReader = await CiqsInputParametersReader.FromHttpRequestMessage(req);

    string name = parametersReader.GetParameter<string>("name");

    return new
    {
        message = $"Hello, {name}!"
    };
}
