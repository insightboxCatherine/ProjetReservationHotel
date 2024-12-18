USE [hotel]
GO
/****** Object:  Table [dbo].[chambre]    Script Date: 2024-09-04 14:40:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[chambre](
	[CHA_roomNumber] [smallint] NOT NULL,
	[CHA_otherInfo] [nvarchar](max) NULL,
	[fk_PKTYP_id] [uniqueidentifier] NOT NULL,
	[PKCHA_roomID] [uniqueidentifier] NOT NULL,
 CONSTRAINT [PK_chambre] PRIMARY KEY CLUSTERED 
(
	[PKCHA_roomID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[client]    Script Date: 2024-09-04 14:40:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[client](
	[CLI_nom] [varchar](50) NOT NULL,
	[CLI_prenom] [varchar](50) NOT NULL,
	[CLI_adresse] [varchar](100) NOT NULL,
	[CLI_mobile] [char](15) NOT NULL,
	[CLI_motDePasse] [char](60) NOT NULL,
	[CLI_courriel] [varchar](50) NOT NULL,
	[PKCLI_id] [uniqueidentifier] NOT NULL,
 CONSTRAINT [PK_client] PRIMARY KEY CLUSTERED 
(
	[PKCLI_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[reservation]    Script Date: 2024-09-04 14:40:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[reservation](
	[RES_startDate] [datetime] NOT NULL,
	[RES_endDate] [datetime] NOT NULL,
	[RES_pricePerDay] [money] NOT NULL,
	[RES_infoReservation] [varchar](max) NULL,
	[PKRES_id] [uniqueidentifier] NOT NULL,
	[fk_PKCLI_id] [uniqueidentifier] NOT NULL,
	[fk_PKCHA_roomID] [uniqueidentifier] NOT NULL,
 CONSTRAINT [PK_reservation] PRIMARY KEY CLUSTERED 
(
	[PKRES_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[type_chambre]    Script Date: 2024-09-04 14:40:53 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[type_chambre](
	[TYP_maxPrice] [money] NULL,
	[TYP_minPrice] [money] NULL,
	[TYP_description] [varchar](200) NULL,
	[TYP_name] [varchar](50) NULL,
	[PKTYP_id] [uniqueidentifier] NOT NULL,
 CONSTRAINT [PK_type_chambre] PRIMARY KEY CLUSTERED 
(
	[PKTYP_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[chambre]  WITH CHECK ADD  CONSTRAINT [FK_chambre_type_chambre] FOREIGN KEY([fk_PKTYP_id])
REFERENCES [dbo].[type_chambre] ([PKTYP_id])
GO
ALTER TABLE [dbo].[chambre] CHECK CONSTRAINT [FK_chambre_type_chambre]
GO
ALTER TABLE [dbo].[reservation]  WITH CHECK ADD  CONSTRAINT [FK_reservation_chambre] FOREIGN KEY([fk_PKCHA_roomID])
REFERENCES [dbo].[chambre] ([PKCHA_roomID])
GO
ALTER TABLE [dbo].[reservation] CHECK CONSTRAINT [FK_reservation_chambre]
GO
ALTER TABLE [dbo].[reservation]  WITH CHECK ADD  CONSTRAINT [FK_reservation_client] FOREIGN KEY([fk_PKCLI_id])
REFERENCES [dbo].[client] ([PKCLI_id])
GO
ALTER TABLE [dbo].[reservation] CHECK CONSTRAINT [FK_reservation_client]
GO
