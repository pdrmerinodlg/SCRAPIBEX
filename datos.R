# --------------------------------------------------------
# FILE: datos.R
# AUTHOR: PEDRO MERINO DELGADO
# MAIL: PDRMERINODLG@GMAIL.COM
# --------------------------------------------------------

#library
library("mongolite")
library(ggplot2)

#data base connection
db <- mongo(collection = "ibex35", db = "crawler", url = "mongodb://XXXX:YYYY@ZZZ.ZZZ.ZZZ")

#mongo query
busqueda<-db$aggregate('[{"$project":
          {
            "fecha": "$fecha",
            "nombre": { "$arrayElemAt": [ "$empresasIBEX.nombre", 7 ] },
            "ultimo": { "$arrayElemAt": [ "$empresasIBEX.ultimo", 7 ] }
          }
      }
   ]')

#data plotting
ggplot(busqueda, aes(reorder(fecha, ultimo), ultimo, group = 1)) +
  geom_point() +
  geom_line() +
  labs(x = "fecha", y = "ultimo", 
       title = busqueda$nombre) +
  theme(axis.text.x = element_text(angle=45, hjust=1, vjust = 1))

