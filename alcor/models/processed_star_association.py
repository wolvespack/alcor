from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger

from .base import Base


class ProcessedStarsAssociation(Base):
    __tablename__ = 'processed_stars_associations'
    original_star_id = Column(BigInteger(),
                              ForeignKey('stars.id'),
                              default=None)
    processed_star_id = Column(BigInteger(),
                               ForeignKey('stars.id'),
                               default=None)

    def __init__(self,
                 original_star_id: int,
                 processed_star_id: int):
        self.original_star_id = original_star_id
        self.processed_star_id = processed_star_id
