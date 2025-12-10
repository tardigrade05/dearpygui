from sqlalchemy import create_engine,String
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column



class Base(DeclarativeBase):
    pass

#id
#category
#value

class Settlement_Model(Base):
    __tablename__ = "settlement"
    id:Mapped[int] = mapped_column(primary_key=True)
    category:Mapped[str] = mapped_column(String(20),default="")
    value:Mapped[str] = mapped_column(String(20),default="")

    

# class ArchivePassenger(Base):
#     __tablename__= "archivepassenger"
#     id:Mapped[int] = mapped_column(primary_key=True)
#     name:Mapped[str] = mapped_column(String(40),default="")
#     email:Mapped[str] = mapped_column(String(20),default="")
#     gender:Mapped[str] = mapped_column(String(10),default="")
#     plane_id:Mapped[str] = mapped_column(String(15),default="")
#     plane_name:Mapped[str] = mapped_column(String(30),default="")
#     seat_number:Mapped[str] = mapped_column(String(5),default="")
#     ticket_number:Mapped[str] = mapped_column(default="")
#     date_departure:Mapped[str] = mapped_column(default="")
#     seat_taken:Mapped[bool] = mapped_column(default=False)