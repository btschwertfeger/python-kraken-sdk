Introduction
=============

This documentation is based on the following documentations and is used to describe methods, functions and classes of the python-kraken-sdk.

- Gerne ein Issue auf github auf machen, wenn etwas nicht korrekt ist oder fehlt ( https://github.com/btschwertfeger/python-kraken-sdk/issues)
- Der Ouput in den Beispielen kann abweichen, da oft auch ein "result" und die serverzeit zurückgeliefert wird
- Falls Ein gewisser endpunkt nicht erreichbar ist, kann auch die Funktion :func:`_request` der Basisklasse
:class:`kraken.base_api.`, welche auch in allen abgeleiteten Klassen zur Verfügung steht verwendet werden, um einen Endpunkt mit den entsprechenden Parametern zu erreichen. Hierbei
kann ebenfalls auf private Inhalte zugegriffen werden, sofern entweder die Basisklasse oder einer der Clients mit validen credentials initialisiert wurde.

References:

    - https://docs.kraken.com/rest
    - https://docs.kraken.com/websockets
    - https://docs.futures.kraken.com
    - https://support.kraken.com/hc/en-us/sections/360012894412-Futures-API
