USE hotel
GO

DECLARE @pk uniqueidentifier
DECLARE @id_type_choisi INT;
DECLARE @uuid_choisi uniqueidentifier;
DECLARE @liste_id_type_chambre table (id int, value uniqueidentifier);

-- Chaque value doit être remplacée par les UID que vous avez généré dans la table [dbo].[type_chambre]
INSERT @liste_id_type_chambre(id, value) VALUES(1,'BAB47532-4879-479D-8D63-22AB75354421'), 
                                               (2,'92CE543B-A5DA-4146-8BCE-29E9212429AE'), 
                                               (3,'93B5128A-3FA9-48F0-A519-437561CB963E'), 
                                               (4,'369B5D93-368C-404E-B5F8-92FFF2786152');

DECLARE @i int = 1;
WHILE @i <= 500
BEGIN
    SET @pk = NEWID()
    SET @id_type_choisi = (SELECT CAST(RAND()*(4-1)+1 AS INT));
    SET @uuid_choisi = (select value from @liste_id_type_chambre where id = @id_type_choisi);

    INSERT INTO [dbo].[chambre]
               ([CHA_roomNumber]
               ,[CHA_availability]
               ,[CHA_otherInfo]
               ,[PKCHA_roomID]
               ,[fk_PKTYP_id])
         VALUES
               (@i
               ,1
               ,NULL
               ,@pk
               ,@uuid_choisi)
    SET @i = @i + 1;
END
GO