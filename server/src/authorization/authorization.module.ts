import { Module } from '@nestjs/common';
import { AuthorizationController } from './authorization.controller';

@Module({
  controllers: [AuthorizationController],
})
export class AuthorizationModule {}
