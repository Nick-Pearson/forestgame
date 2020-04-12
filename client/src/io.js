function Response(status, body)
{
  this.status = status;
  this.body = body;
}

function parseJsonOrNull(string)
{
  try
  {
    return JSON.parse(string);
  }
  catch (e)
  {
    return null;
  }
}

function restRequest(req, onResponse)
{
  console.log("New REST request " + req.method + " /api" + req.path);
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function()
  {
    if (this.readyState == 4)
    {
      const responseBody = parseJsonOrNull(this.responseText);
      onResponse(new Response(this.status, responseBody));
    }
  };
  xhttp.open(req.method, "/api" + req.path, true);
  if (req.body !== undefined && req.body != null)
  {
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(JSON.stringify(req.body));
  }
  else
  {
    xhttp.send();
  }
}

export {restRequest};
