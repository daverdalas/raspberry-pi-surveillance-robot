import {
  Controller,
  HttpCode,
  Post,
  Body,
  UnauthorizedException,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Controller('authorization')
export class AuthorizationController {
  constructor(private configService: ConfigService) {}

  @Post('stream')
  @HttpCode(200)
  stream(@Body('param') param: string): number {
    const params = new URLSearchParams(param);
    const username = params.get('username');
    const password = params.get('password');

    if (
      username !== this.configService.get<string>('authorization.username') ||
      password !== this.configService.get<string>('authorization.password')
    ) {
      throw new UnauthorizedException();
    }

    return 0;
  }
}
