USE [Group5HWMart]
GO

-- DROP CONSTRAINT

ALTER TABLE [Time]
DROP CONSTRAINT [PK_Time]

ALTER TABLE [Cpu_sales]
DROP CONSTRAINT [FK_Cpu_sales_Time]

ALTER TABLE [Gpu_sales]
DROP CONSTRAINT [FK_Gpu_sales_Time]

ALTER TABLE [Ram_sales]
DROP CONSTRAINT [FK_Ram_sales_Time]


-- Alter Column Data Type

ALTER TABLE [Time]
ALTER COLUMN [time_code] DATE NOT NULL

ALTER TABLE [Cpu_sales]
ALTER COLUMN [time_code] DATE NOT NULL

ALTER TABLE [Gpu_sales]
ALTER COLUMN [time_code] DATE NOT NULL

ALTER TABLE [Ram_sales]
ALTER COLUMN [time_code] DATE NOT NULL


-- ADD CONSTRAINT again

ALTER TABLE [Time]
ADD CONSTRAINT [PK_Time] PRIMARY KEY CLUSTERED ([time_code] ASC)

ALTER TABLE [Cpu_sales]
ADD CONSTRAINT [FK_Cpu_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])

ALTER TABLE [Gpu_sales]
ADD CONSTRAINT [FK_Gpu_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])

ALTER TABLE [Ram_sales]
ADD CONSTRAINT [FK_Ram_sales_Time] FOREIGN KEY ([time_code]) REFERENCES [group5].[Time] ([time_code])

