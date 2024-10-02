USE [hotel]
GO
DECLARE @id uniqueidentifier
SET @id = NEWID()



SET @id = NEWID()
            INSERT INTO [dbo].[type_chambre]
                   ([TYP_maxPrice]
                   ,[TYP_minPrice]
                   ,[TYP_description]
                   ,[TYP_name]
                   ,[PKTYP_id])
             VALUES
                   (199
                   ,99
                   ,'chambre avec un lit simple'
                   ,'simple'
                   ,@id)


SET @id = NEWID()
    INSERT INTO [dbo].[type_chambre]
               ([TYP_maxPrice]
               ,[TYP_minPrice]
               ,[TYP_description]
               ,[TYP_name]
               ,[PKTYP_id])
         VALUES
               (299
               ,199
               ,'chambre avec un lit double'
               ,'double'
               ,@id)


SET @id = NEWID()
    INSERT INTO [dbo].[type_chambre]
               ([TYP_maxPrice]
               ,[TYP_minPrice]
               ,[TYP_description]
               ,[TYP_name]
               ,[PKTYP_id])
         VALUES
               (399
               ,299
               ,'chambre avec un lit Queen'
               ,'Queen'
               ,@id)


SET @id = NEWID()
        INSERT INTO [dbo].[type_chambre]
                   ([TYP_maxPrice]
                   ,[TYP_minPrice]
                   ,[TYP_description]
                   ,[TYP_name]
                   ,[PKTYP_id])
             VALUES
                   (499
                   ,399
                   ,'chambre avec un lit king'
                   ,'king'
                   ,@id)
GO