class EventBroadcast
{
  constructor(name)
  {
    this.name = name;
    this._listeners = [];
  }

  broadcast()
  {
    this._listeners.forEach((l) =>
    {
      try
      {
        l();
      }
      catch (e)
      {
        console.error("error dispatching " + name + " event", e);
      }
    });
  }

  addListener(func)
  {
    this._listeners.push(func);
  }
}

export {EventBroadcast};
