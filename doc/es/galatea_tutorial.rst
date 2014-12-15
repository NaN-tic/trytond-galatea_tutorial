.. inheritref:: galatea_tutorial/galatea:section:tutoriales

----------
Tutoriales
----------

Esta App dispone la funcionalidad de la generación de tutoriales.

Para la gestión de tutoriales accede a |menu_galatea_tutorial|. Como todo registro
web deberá tener en cuenta:

* Slug: Es el ID o clave del vuestro registro. Sólo debe usar los carácteres az09-
  (sin acentos ni espacios). Este campo debe ser único ya que no pueden haber más
  de dos o más slugs en sus empleados. Recuerde que es un campo multi idioma.
  Cuando introduzca un título se le propone un slug a partir del título que después
  lo podrá cambiar. Un slug podría ser 'mi-tutorial-sobre-tryton' y crearia una dirección como
  http://www.midominio.com/es/tutorial/mi-tutorial-sobre-tryton
* SEO MetaKeyword. Introduce las palabras clave de su tutorial separados por comas
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaKeyword
  podría ser "tryton,configuración,contabilidad". Recuerde que es un campo multi idioma.
* SEO MetaDescription. Introduce una descripción breve del artículo (el resumen)
  (no más de 155 carácteres) que se usará para los buscadores. Un ejemplo de MetaDescription
  podria ser "Configuración pagos SEPA en Tryton". Recuerde que es un
  campo multi idioma.
* SEO MetaTitle. Si el título del tutorial en los buscadores desea que sea diferente del nombre
  del empleado puede usar este campo para cambiarlo. Recuerde que es un campo multi idioma.

Para el contenido de un tutorial puede usar los campos descripciones. Usa el campo "Descripción larga"
para descripciones con contenido extenso. Para el formato HTML usa los tags de Wiki para dar formato a su contendido.
Los tags de wiki le permite formatear el texto para después sea mostrado con HTML. Para
información de los tags de wiki puede consultar `MediaWiki <http://meta.wikimedia.org/wiki/Help:Editing>`_

Como siempre recuerde que si edita un empleado y su web es multi idioma, debe de cambiar
el contenido por cada idioma con el campo de la "bandera".

Para acceder a un empleado en concreto accede a:

* Español: http://www.midominio.com/es/tutorial/<SLUG>
* Catalan: http://www.midominio.com/ca/tutorial/<SLUG>
* Inglés: http://www.midominio.com/en/tutorial/<SLUG>

.. inheritref:: galatea_tutorial/galatea:section:todos_tutoriales

Todos los tutoriales
--------------------

Como toda app dispone de un listado de todos los tutoriales. Estos siempre
se listaran por el nombre en orden ascendiente.

Para acceder a todos los tutoriales accede a:

* Español: http://www.midominio.com/es/tutorial/
* Catalan: http://www.midominio.com/ca/tutorial/
* Inglés: http://www.midominio.com/en/tutorial/

.. |menu_galatea_tutorial| tryref:: galatea_tutorial.menu_galatea_tutorial/complete_name
