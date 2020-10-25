USE [Group5HWMart]
GO

-- Creazione Dimension Tables

CREATE TABLE [group5].[Cpu_product] (
    [cpu_code] INT          NOT NULL,
    [brand]    VARCHAR (50) NULL,
    [series]   VARCHAR (50) NULL,
    [name]     VARCHAR (50) NULL,
    [n_cores]  INT          NULL,
    [socket]   VARCHAR (50) NULL,
    CONSTRAINT [PK_Cpu_product] PRIMARY KEY CLUSTERED ([cpu_code] ASC)
);

CREATE TABLE [group5].[Gpu_product] (
    [gpu_code]               INT          NOT NULL,
    [processor]              VARCHAR (50) NULL,
    [processor_manufacturer] VARCHAR (50) NULL,
    [brand]                  VARCHAR (50) NULL,
    [memory]                 FLOAT (53)   NULL,
    [memory_type]            VARCHAR (50) NULL,
    CONSTRAINT [PK_Gpu_product] PRIMARY KEY CLUSTERED ([gpu_code] ASC)
);

CREATE TABLE [group5].[Ram_product] (
    [ram_code]    INT          NOT NULL,
    [brand]       VARCHAR (50) NULL,
    [name]        VARCHAR (50) NULL,
    [memory]      FLOAT (53)   NULL,
    [memory_type] VARCHAR (50) NULL,
    [clock]       INT          NULL,
    CONSTRAINT [PK_Ram_product] PRIMARY KEY CLUSTERED ([ram_code] ASC)
);

CREATE TABLE [group5].[Time] (
    [time_code]   DATE         NOT NULL,
    [year]        INT		   NULL,
    [quarter]     VARCHAR (50) NULL,
    [month]       INT          NULL,
    [week]        INT          NULL,
    [day]         INT          NULL,
    [day_of_week] VARCHAR (50) NULL,
    CONSTRAINT [PK_Time] PRIMARY KEY CLUSTERED ([time_code] ASC)
);

CREATE TABLE [group5].[Vendor] (
    [vendor_code] INT          NOT NULL,
    [name]        VARCHAR (50) NULL,
    CONSTRAINT [PK_Vendor] PRIMARY KEY CLUSTERED ([vendor_code] ASC)
);

CREATE TABLE [group5].[Geography] (
    [geo_code]  INT          NOT NULL,
    [continent] VARCHAR (50) NULL,
    [country]   VARCHAR (50) NULL,
    [region]    VARCHAR (50) NULL,
    [currency]  VARCHAR (50) NULL,
    CONSTRAINT [PK_Geography] PRIMARY KEY CLUSTERED ([geo_code] ASC)
);


-- Creazione Fact Tables

CREATE TABLE [group5].[Cpu_sales] (
    [cpu_code]       INT        NOT NULL,
    [time_code]      DATE       NOT NULL,
    [geo_code]       INT        NOT NULL,
    [vendor_code]    INT        NOT NULL,
    [sales_usd]      BIGINT     NOT NULL,
    [sales_currency] FLOAT (53) NOT NULL,
    CONSTRAINT [FK_Cpu_sales_Cpu_product] FOREIGN KEY ([cpu_code]) REFERENCES [group5].[Cpu_product] ([cpu_code]),
    CONSTRAINT [FK_Cpu_sales_Geography] FOREIGN KEY ([geo_code]) REFERENCES [group5].[Geography] ([geo_code]),
    CONSTRAINT [FK_Cpu_sales_Vendor] FOREIGN KEY ([vendor_code]) REFERENCES [group5].[Vendor] ([vendor_code]),
    CONSTRAINT [FK_Cpu_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])
);

CREATE TABLE [group5].[Gpu_sales] (
    [gpu_code]       INT        NOT NULL,
    [time_code]      DATE       NOT NULL,
    [geo_code]       INT        NOT NULL,
    [vendor_code]    INT        NOT NULL,
    [sales_usd]      BIGINT     NOT NULL,
    [sales_currency] FLOAT (53) NOT NULL,
    CONSTRAINT [FK_Gpu_sales_Gpu_product] FOREIGN KEY ([gpu_code]) REFERENCES [group5].[Gpu_product] ([gpu_code]),
    CONSTRAINT [FK_Gpu_sales_Geography] FOREIGN KEY ([geo_code]) REFERENCES [group5].[Geography] ([geo_code]),
    CONSTRAINT [FK_Gpu_sales_Vendor] FOREIGN KEY ([vendor_code]) REFERENCES [group5].[Vendor] ([vendor_code]),
    CONSTRAINT [FK_Gpu_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])
);

CREATE TABLE [group5].[Ram_sales] (
    [ram_code]       INT        NOT NULL,
    [time_code]      DATE       NOT NULL,
    [geo_code]       INT        NOT NULL,
    [vendor_code]    INT        NOT NULL,
    [sales_usd]      BIGINT     NOT NULL,
    [sales_currency] FLOAT (53) NOT NULL,
    CONSTRAINT [FK_Ram_sales_Ram_product] FOREIGN KEY ([ram_code]) REFERENCES [group5].[Ram_product] ([ram_code]),
    CONSTRAINT [FK_Ram_sales_Geography] FOREIGN KEY ([geo_code]) REFERENCES [group5].[Geography] ([geo_code]),
    CONSTRAINT [FK_Ram_sales_Vendor] FOREIGN KEY ([vendor_code]) REFERENCES [group5].[Vendor] ([vendor_code]),
    CONSTRAINT [FK_Ram_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])
);