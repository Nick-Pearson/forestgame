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

function restRequest(method, path, onResponse)
{
  console.log("New REST request " + method + " /api" + path);
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function()
  {
    if (this.readyState == 4)
    {
      const responseBody = parseJsonOrNull(this.responseText);
      onResponse(new Response(this.status, responseBody));
    }
  };
  xhttp.open(method, "/api" + path, true);
  xhttp.send();
}

export {restRequest};
